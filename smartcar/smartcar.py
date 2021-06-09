from . import api, const, requester, vehicle
import re
import time
from datetime import datetime, timedelta
from urllib.parse import urlencode

API_VERSION = "2.0"
AUTH_VERSION = "1.0"


def set_expiration(access):
    expire_date = datetime.utcnow() + timedelta(seconds=access["expires_in"])
    refresh_expire_date = datetime.utcnow() + timedelta(days=60)
    access["expiration"] = expire_date
    access["refresh_expiration"] = refresh_expire_date
    return access


def is_expired(expiration):
    """Check if an expiration is expired

    Args:
        expiration (datetime): expiration datetime

    Returns:
        bool: true if expired
    """
    return datetime.utcnow() > expiration


def set_api_version(version: str) -> None:
    """Update the version of Smartcar API you are using

    Args:
        version (str): the version of the api you want to use
    """
    if re.match('\d+\.\d+', version):
        global API_VERSION
        API_VERSION = version
    else:
        raise ValueError(
            f"Version '{version}' must match regex '\d+\.\d+' .  e.g. '2.0', '1.0'")


def set_auth_version(version: str) -> None:
    """Update the Authentication version you are using

    *Not yet implemented

    Args:
        version (str): the version of auth you want to use
    """
    if re.match('\d+\.\d+', version):
        global AUTH_VERSION
        AUTH_VERSION = version
    else:
        raise ValueError(
            f"Version '{version}' must match regex '\d+\.\d+' .  e.g. '2.0', '1.0'")


def get_vehicles(access_token, paging={"limit": 10, "offset": 0}):
    """Get a list of the user's vehicle ids

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
    limit = paging['limit']
    offset = paging['offset']
    return api.Api(access_token).vehicles(limit=limit, offset=offset).json()


def get_user(access_token: str):
    """Retrieve the userId associated with the access_token

    Args:
        access_token (str): Smartcar access token

    Returns:
        { "id" : <id> }

    Raises:
        SmartcarException

    """
    return api.Api(access_token).user().json()["id"]


class AuthClient(object):
    def __init__(
        self,
        client_id,
        client_secret,
        redirect_uri,
        test_mode=None,
        flags=None,
        version='2.0',
        origin=None
    ):
        """A client for accessing the Smartcar API

        Args:
            client_id (str): The application id, provided in the application
                dashboard
            client_secret (str): The application secret, provided in the
                application dashboard
            redirect_uri (str): The URL to redirect to after the user accepts
                or declines the application's permissions. This URL must also be
                present in the Redirect URIs field in the application dashboard
            test_mode (bool, optional): Launch the Smartcar auth flow in test mode. Defaults to false.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth = (client_id, client_secret)
        self.redirect_uri = redirect_uri
        self.test_mode = test_mode if test_mode else False
        self.version = version

    def get_auth_url(
        self, scope, force=False, state=None, make_bypass=None, single_select=None, flags=None
    ):
        """Generate the Connect URL

        Args:
            scope (str[], required): A list of permissions requested by the application
            force (bool, optional): Set to True in order to force the approval
                dialog shown to the user. Defaults to False.
            state (bool, optional): A random string that will be passed back on
                redirect, this allows protection against cross-site forgery
                requests. Defaults to None.
            make_bypass (str, optional): A string that represents a make(car brand). Allows
                users to bypass the car brand selection screen, allowing the
                user to go directly to the vehicle login screen.
                Defaults to None.
            single_select (bool or dictionary, optional): An optional value that
                sets the behavior of the grant dialog displayed to the user. It
                can be either a bool or dict. If set to True, `single_select`
                limits the user to selecting only one vehicle. If `single_select`
                is a dictionary with the property `vin`, Smartcar will only authorize the vehicle
                with the specified VIN. See the [Single Select guide](https://smartcar.com/docs/guides/single-select/)
                for more information. Defaults to None.
            flags (str[], optional): List of feature flags that your application has early access to.

        Returns:
            str: authorization url

        Raises:
            SmartcarException

        """
        base_url = const.CONNECT_URL

        approval_prompt = "force" if force else "auto"
        query = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "approval_prompt": approval_prompt,
        }

        query["scope"] = " ".join(scope)

        if self.test_mode:
            query["mode"] = "test"

        if state:
            query["state"] = state

        if make_bypass:
            query["make"] = make_bypass

        if single_select is not None:
            query["single_select"] = False
            if isinstance(single_select, dict):
                valid_parameters = ["vin"]
                for param in valid_parameters:
                    if param in single_select:
                        query["single_select_" + param] = single_select[param]
                        query["single_select"] = True
            else:
                query["single_select"] = single_select == True

        if flags:
            query["flags"] = " ".join(flags)

        return base_url + "/oauth/authorize?" + urlencode(query)

    def exchange_code(self, code):
        """Exchange an authentication code for an access dictionary

        Args:
            code (str): A valid authorization code

        Returns:
            dict: dict containing the access and refresh token

        Raises:
            SmartcarException

        """
        method = "POST"
        url = const.AUTH_URL
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
        }
        response = requester.call(
            method, url, data=data, auth=self.auth).json()
        return set_expiration(response)

    def exchange_refresh_token(self, refresh_token):
        """Exchange a refresh token for a new access dictionary

        Args:
            refresh_token (str): A valid refresh token from a previously retrieved
                access object

        Returns:
            dict: dict containing access and refresh token

        Raises:
            SmartcarException

        """
        method = "POST"
        url = const.AUTH_URL
        data = {"grant_type": "refresh_token", "refresh_token": refresh_token}
        response = requester.call(
            method, url, data=data, auth=self.auth).json()
        return set_expiration(response)

    def is_compatible(self, vin, scope, country="US"):
        """Determine if a vehicle is compatible with Smartcar

        Args:
            vin (str): the VIN of the vehicle
            scope (list): list of permissions to return compatibility info for
            country (str, optional): country code according to [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) of the provided vin

        Returns:
            boolean: true if the vehicle is compatible

        Raises:
            SmartcarException

        """
        method = "GET"
        url = "{}/v{}/compatibility".format(const.API_URL, API_VERSION)
        query = {"vin": vin, "scope": " ".join(scope), "country": country}

        response = requester.call(
            method, url, params=query, auth=self.auth).json()
        return response["compatible"]
