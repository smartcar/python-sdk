from datetime import datetime, timedelta
from typing import List
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
        self.origin = origin if origin else constants.AUTH_URL

    def get_auth_url(self, scope: List[str], options: dict = None):
        """
        Generate the Connect URL

        Args:
            scope (str[], required): A list of permissions requested by the application
            options (dict, optional): Can have the following keys:
                force_prompt (bool, optional): Set to True in order to force the approval
                    dialog shown to the user. Defaults to False.
                state (str, optional): A random string that will be passed back on
                    redirect, this allows protection against cross-site forgery
                    requests. Defaults to None.
                make_bypass (str, optional): A string that represents a make(car brand).
                    Allows users to bypass the car brand selection screen, allowing the
                    user to go directly to the vehicle login screen. Defaults to None.
                single_select (dictionary, optional): An optional value that
                    sets the behavior of the grant dialog displayed to the user.
                    Can have keys of enabled(bool) and vin(str).
                    if options['enabled'] == True, `single_select`
                    limits the user to selecting only one vehicle. If `single_select`
                    contains a property of `vin`, Smartcar will only authorize the vehicle
                    with the specified VIN. See the [Single Select guide](https://smartcar.com/docs/guides/single-select/)
                    for more information. Defaults to None.
                flags:

        Returns:
            str: authorization url

        Raises:
            SmartcarException
        """
        base_url = constants.CONNECT_URL

        query = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "approval_prompt": "auto",
            "scope": " ".join(scope),
        }
        if self.test_mode:
            query["mode"] = "test"

        if options:
            if options.get("force_prompt"):
                query["approval_prompt"] = "force"

            if options.get("state"):
                query["state"] = options["state"]

            if options.get("make_bypass"):
                query["make"] = options["make_bypass"]

            if options.get("single_select"):
                single_select = options["single_select"]

                if single_select.get("vin"):
                    query['single_select"vin'] = single_select["vin"]
                    query["single_select"] = True
                elif single_select.get("enabled"):
                    query["single_select"] = True
                else:
                    query["single_select"] = False

            if options.get("flags"):
                query["flags"] = " ".join(options["flags"])

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
