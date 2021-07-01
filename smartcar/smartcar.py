import base64
import hmac
import hashlib
import os
from datetime import datetime
from typing import List

import smartcar.config as config
import smartcar.helpers as helpers
import smartcar.types as types


def get_user(access_token: str) -> types.User:
    """
    Retrieve the userId associated with the access_token

    Args:
        access_token (str): Smartcar access token

    Returns:
        User: NamedTuple("User", [("id", str), ("meta", namedtuple)])

    Raises:
        SmartcarException
    """
    url = f"{config.API_URL}/v{config.API_VERSION}/user"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = helpers.requester("GET", url, headers=headers)

    return types.select_named_tuple("user", response)


def get_vehicles(access_token: str, paging: dict = None) -> types.Vehicles:
    """
    Get a list of the user's vehicle ids

    Args:
        access_token (str): A valid access token from a previously retrieved
            access object

        paging (dictionary, optional): Can include "limit" and "offset" keys:
            limit (int, optional): The number of vehicle ids to return
            offset (int, optional): The index to start the vehicle list at

    Returns:
        Vehicles: NamedTuple("Vehicles", [("vehicles", List[str]), ("paging", Paging), ("meta", namedtuple)])

    Raises:
        SmartcarException
    """
    url = f"{config.API_URL}/v{config.API_VERSION}/vehicles"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = paging if paging is not None else None
    response = helpers.requester("GET", url, headers=headers, params=params)

    return types.select_named_tuple("vehicles", response)


def get_compatibility(
    vin: str, scope: List[str], country: str = "US", options: dict = None
) -> types.Compatibility:
    """
    Verify if a vehicle (vin) is eligible to use Smartcar. Use to confirm whether
    specific vehicle is compatible with the permissions provided.

    A compatible vehicle is one that:
        1. Has hardware required for internet connectivity
        2. Belongs to the makes and models Smartcar is compatible with
        3. Is compatible with the required permissions (scope) that your app is requesting
            access to

    Args:
        vin (str)
        scope (List[str]): List of scopes (permissions) -> to check if vehicle is compatible
        country (str, optional)
        options (dictionary): Can contain client_id, client_secret, and flags.
            client_id (str, optional)
            client_secret (str, optional)
            version (str): Version of API you want to use
            flags: dictionary(str, bool): An optional list of feature flags


    Returns:
        Compatibility: NamedTuple("Compatibility", [("compatible", bool), ("meta", namedtuple)])
    """
    client_id = os.environ.get("SMARTCAR_CLIENT_ID")
    client_secret = os.environ.get("SMARTCAR_CLIENT_SECRET")
    api_version = config.API_VERSION
    params = {"vin": vin, "scope": " ".join(scope), "country": country}

    # Configuring options.
    if options is None:
        helpers.validate_env()
    else:
        # client_id and client_secret passed in options dict() will take precedence
        # over environment variables.
        client_id = options.get("client_id", client_id)
        client_secret = options.get("client_secret", client_secret)
        api_version = options.get("version", api_version)

        if options.get("flags"):
            flags_str = helpers.format_flag_query(options["flags"])
            params["flags"] = flags_str

    # Ensuring client_id and client_secret are present
    if client_id is None or client_secret is None:
        raise Exception(
            "'get_compatibility' requires a client_id AND client_secret. "
            "Either set these as environment variables, OR pass them in as part of the 'options'"
            "dictionary. The recommended course of action is to set up environment variables"
            "with your client credentials. i.e.: "
            "'SMARTCAR_CLIENT_ID' and 'SMARTCAR_CLIENT_SECRET'"
        )

    url = f"{config.API_URL}/v{api_version}/compatibility"

    # Configuring for compatibility endpoint
    id_secret = f"{client_id}:{client_secret}"
    encoded_id_secret = id_secret.encode("ascii")
    base64_bytes = base64.b64encode(encoded_id_secret)
    base64_id_secret = base64_bytes.decode("ascii")
    headers = {"Authorization": f"Basic {base64_id_secret}"}

    response = helpers.requester("GET", url, headers=headers, params=params)
    return types.select_named_tuple("compatibility", response)


def is_expired(expiration: datetime) -> bool:
    """
    Check if an expiration is expired.
    This helper method can be used on the 'expiration' or 'refresh_expiration'
    values from the 'access object' received after going through Smartcar
    Connect Auth flow.

    Args:
        expiration (datetime): expiration datetime

    Returns:
        bool: true if expired
    """
    return datetime.utcnow() > expiration


# ===========================================
# Webhook functions
# ===========================================


def hash_challenge(amt: str, challenge: str) -> str:
    """
    Take in a randomly generated challenge string, and use an
    Application Management Token as a key to be hashed.

    Args:
        amt (str): Application Management Token from Smartcar Dashboard
        challenge: Randomly generated string from smartcar after requesting
            a challenge.

    Returns:
        hex-encoding of resulting hash
    """
    h = hmac.new(amt.encode(), challenge.encode(), hashlib.sha256)
    return h.hexdigest()


def verify_payload(amt: str, signature: str, body: str) -> bool:
    """
    Verify webhook payload against AMT and signature

    Args:
        amt (str): Application Management Token from Smartcar Dashboard
        signature: sc-signature header value
        body: Stringified JSON of the webhook response body

    Returns:
        Boolean
    """
    return hash_challenge(amt, body) == signature
