import re
from typing import List

import smartcar.api as api
import smartcar.helpers as helpers

API_VERSION = "2.0"


def set_api_version(version: str) -> None:
    """
    Update the version of Smartcar API you are using

    Args:
        version (str): the version of the api you want to use
    """
    if re.match("\d+\.\d+", version):
        global API_VERSION
        API_VERSION = version
    else:
        raise ValueError(
            f"Version '{version}' must match regex '\d+\.\d+' .  e.g. '2.0', '1.0'"
        )


def get_user(access_token: str) -> dict:
    """
    Retrieve the userId associated with the access_token

    Args:
        access_token (str): Smartcar access token

    Returns:
        { "id" : <id> }

    Raises:
        SmartcarException
    """
    response = api.Smartcar(access_token).user()
    user_id = response.json()["id"]

    return {"id": user_id}


def get_vehicles(access_token, paging=None):
    """
    Get a list of the user's vehicle ids

    Args:
        access_token (str): A valid access token from a previously retrieved
            access object
        limit (integer, optional): The number of vehicle ids to return
        offset (integer, optional): The index to start the vehicle list at

    Returns:
        dict: response containing the list of vehicle ids and paging information

    Raises:
        SmartcarException
    """
    if paging is None:
        paging = {"limit": 10, "offset": 0}

    limit = paging["limit"]
    offset = paging["offset"]
    return api.Smartcar(access_token).vehicles(limit=limit, offset=offset).json()


def get_compatibility(access_token, vin: str, scope: List[str], country: str = 'US', options: dict = None):
    helpers.validate_env()
    scope_param = " ".join(scope)

    return api.Smartcar(access_token).compatibility(vin=vin, scope=scope_param, country=country).json()
