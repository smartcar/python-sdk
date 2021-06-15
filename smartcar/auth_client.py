from datetime import datetime, timedelta
from urllib.parse import urlencode

import smartcar.constants as constants
import smartcar.requester as requester


class AuthClient(object):
    def __init__(
            self,
            client_id,
            client_secret,
            redirect_uri,
            test_mode=None,
            flags=None,
            version="2.0",
            origin=None,
    ):
        """
        A client for accessing the Smartcar API

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
            self,
            scope,
            force=False,
            state=None,
            make_bypass=None,
            single_select=None,
            flags=None,
    ):
        """
        Generate the Connect URL

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
        base_url = constants.CONNECT_URL

        approval_prompt = "force" if force else "auto"
        query = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "approval_prompt": approval_prompt,
            "scope": " ".join(scope)
        }

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
        """
        Exchange an authentication code for an access dictionary

        Args:
            code (str): A valid authorization code

        Returns:
            dict: dict containing the access and refresh token

        Raises:
            SmartcarException
        """
        method = "POST"
        url = constants.AUTH_URL
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
        }
        response = requester.call(method, url, data=data, auth=self.auth).json()
        return _set_expiration(response)

    def exchange_refresh_token(self, refresh_token):
        """
        Exchange a refresh token for a new access dictionary

        Args:
            refresh_token (str): A valid refresh token from a previously retrieved
                access object

        Returns:
            dict: dict containing access and refresh token

        Raises:
            SmartcarException
        """
        method = "POST"
        url = constants.AUTH_URL
        data = {"grant_type": "refresh_token", "refresh_token": refresh_token}
        response = requester.call(method, url, data=data, auth=self.auth).json()
        return _set_expiration(response)

    def is_compatible(self, vin, scope, country="US"):
        """
        Determine if a vehicle is compatible with Smartcar

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
        url = "{}/v{}/compatibility".format(constants.API_URL, API_VERSION)
        query = {"vin": vin, "scope": " ".join(scope), "country": country}

        response = requester.call(method, url, params=query, auth=self.auth).json()
        return response["compatible"]


# Static helpers for AuthClient

def _set_expiration(access):
    expire_date = datetime.utcnow() + timedelta(seconds=access["expires_in"])
    refresh_expire_date = datetime.utcnow() + timedelta(days=60)
    access["expiration"] = expire_date
    access["refresh_expiration"] = refresh_expire_date
    return access
