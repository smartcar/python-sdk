import re
from typing import List

import smartcar.api as api
import smartcar.helpers as helpers
import smartcar.types as ty

API_VERSION = "2.0"


def set_api_version(version: str) -> None:
    """
    Update the version of Smartcar API you are using

    Args:
        version (str): the version of the api you want to use
    """
    if re.match(r"\d+\.\d+", version):
        global API_VERSION
        API_VERSION = version
    else:
        raise ValueError(
            fr"Version '{version}' must match regex '\d+\.\d+' .  e.g. '2.0', '1.0'"
        )


def get_user(access_token: str) -> ty.User:
    """
    Retrieve the userId associated with the access_token

    Args:
        access_token (str): Smartcar access token

    Returns:
        User: NamedTuple("User", [("id", str), ("meta", Meta)])

    Raises:
        SmartcarException
    """
    response = api.Smartcar(access_token).user()
    data = response.json()
    result = ty.User(data["id"], ty.Meta(**response.headers))
    return result


def get_vehicles(access_token: str, paging: dict = None) -> ty.Vehicles:
    """
    Get a list of the user's vehicle ids

    Args:
        access_token (str): A valid access token from a previously retrieved
            access object

        paging (dictionary, optional): Can include "limit" and "offset" keys:
            limit (int, optional): The number of vehicle ids to return
            offset (int, optional): The index to start the vehicle list at

    Returns:
        Vehicles: NamedTuple("Vehicles", [("vehicles", List[str]), ("paging", Paging), ("meta", Meta)])

    Raises:
        SmartcarException
    """
    if paging is None:
        paging = {"limit": 10, "offset": 0}

    limit = paging.get("limit")
    offset = paging.get("offset")
    response = api.Smartcar(access_token).vehicles(limit=limit, offset=offset)
    data = response.json()
    result = ty.Vehicles(data["vehicles"], ty.Paging(data["paging"]["count"], data["paging"]["offset"]),
                         ty.Meta(**response.headers))
    return result


def get_compatibility(
        access_token,
        vin: str,
        scope: List[str],
        country: str = "US",
        options: dict = None) -> ty.Compatibility:
    """
    Verify if a vehicle (vin) is eligible to use Smartcar. Use to confirm whether
    specific vehicle is compatible with the permissions provided.

    A compatible vehicle is one that:
        1. Has hardware required for internet connectivity
        2. Belongs to the makes and models Smartcar is compatible with
        3. Is compatible with the required permissions (scope) that your app is requesting
            access to

    Args:
        access_token (str)
        vin (str)
        scope (List[str]): List of scopes (permissions) -> to check if vehicle is compatible
        country (str, optional)
        options (dictionary): Can contain client_id and client_secret. Technically, they are
            both optional, but if using a client_id other than the one provided through
            environment variables, it'll be likely that a client_secret will have to be
            provided. Regardless, authentication will be verified.

    Returns:
        Compatibility: NamedTuple("Compatibility", [("compatible", bool), ("meta", Meta)])
    """
    sc_api = api.Smartcar(access_token)

    if options is None:
        helpers.validate_env()
    else:
        if options.get("client_id"):
            sc_api.set_env_custom(client_id=options["client_id"])

        if options.get("client_secret"):
            sc_api.set_env_custom(client_secret=options["client_secret"])

    scope_param = " ".join(scope)

    response = sc_api.compatibility(vin=vin, scope=scope_param, country=country)
    data = response.json()
    result = ty.Compatibility(data["compatible"], ty.Meta(**response.headers))
    return result
