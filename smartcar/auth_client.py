import os
from datetime import datetime, timedelta
from typing import List
from urllib.parse import urlencode

import smartcar.config as config
import smartcar.helpers as helpers
import smartcar.types as types


class AuthClient(object):
    def __init__(
        self,
        client_id=None,
        client_secret=None,
        redirect_uri=None,
        test_mode=False,
    ):
        """
        A client for accessing the Smartcar API.

        NOTE: It is recommended that you set environment variables with your client id, secret, and redirect URI.
        AuthClient by default will search for environment variables "SMARTCAR_CLIENT_ID",
        "SMARTCAR_CLIENT_SECRET", and "SMARTCAR_REDIRECT_URL" and set those as attributes.
        These CAN be passed as arguments as you instantiate AuthClient. Any arguments passed in will override
        and take precedence over the corresponding environment variable.

        However, if neither an environment variable nor an argument is passed in, an exception will be raised.

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
        self.client_id = client_id or os.environ.get("SMARTCAR_CLIENT_ID")
        self.client_secret = client_secret or os.environ.get("SMARTCAR_CLIENT_SECRET")
        self.redirect_uri = redirect_uri or os.environ.get("SMARTCAR_REDIRECT_URI")
        self.test_mode = test_mode
        self.auth = (self.client_id, self.client_secret)

        if (
            self.client_id is None
            or self.client_secret is None
            or self.redirect_uri is None
        ):
            raise Exception(
                "AuthClient MUST have client_id, client_secret, and redirect_uri attributes."
                "Either set these as environment variables, OR pass them in as arguments when instantiating "
                "AuthClient. The recommended course of action is to set up environment variables "
                "with your client credentials. i.e.: "
                "'SMARTCAR_CLIENT_ID', 'SMARTCAR_CLIENT_SECRET', and 'SMARTCAR_REDIRECT_URI'"
            )

    def get_auth_url(self, scope: List[str], options: dict = None) -> str:
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
                    limits the user to selecting only one vehicle. If `single_select` contains a property
                    of `vin`, Smartcar will only authorize the vehicle with the specified VIN.
                    See the [Single Select guide](https://smartcar.com/docs/guides/single-select/)
                    for more information. Defaults to None.

                flags: dictionary(str, bool): An optional list of feature flags that your
                    application has early access to.

        Returns:
            str: authorization url

        Raises:
            SmartcarException
        """
        base_url = config.CONNECT_URL

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
                    query["single_select_vin"] = single_select["vin"]
                    query["single_select"] = True
                elif single_select.get("enabled"):
                    query["single_select"] = True
                else:
                    query["single_select"] = False

            if options.get("flags"):
                flags_str = helpers.format_flag_query(options["flags"])
                query["flags"] = flags_str

        return base_url + "/oauth/authorize?" + urlencode(query)

    def exchange_code(self, code: str, options: dict = None) -> types.Access:
        """
        Exchange an authentication code for an access dictionary

        Args:
            code (str): A valid authorization code

            options (dict, optional): Can have the following keys:

                flags: dictionary(str, bool): An optional list of feature flags that your
                    application has early access to.

        Returns:
            Access: containing access information, including access_token and
                refresh_token

        Raises:
            SmartcarException
        """
        method = "POST"
        url = config.AUTH_URL
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
        }
        params = {}

        if options:
            if options.get("flags"):
                flags_str = helpers.format_flag_query(options["flags"])
                params["flags"] = flags_str

        response = helpers.requester(
            method, url, data=data, auth=self.auth, params=params
        )
        data = response.json()
        return types.make_access_object(_set_expiration(data))

    def exchange_refresh_token(
        self, refresh_token: str, options: dict = None
    ) -> types.Access:
        """
        Exchange a refresh token for a new access dictionary

        Args:
            refresh_token (str): A valid refresh token from a previously retrieved
                access object

            options (dict, optional): Can have the following keys:
                flags: dictionary(str, bool): An optional list of feature flags that your
                    application has early access to.

        Returns:
            Access: containing access information, including access_token and
                refresh_token

        Raises:
            SmartcarException
        """
        method = "POST"
        url = config.AUTH_URL
        data = {"grant_type": "refresh_token", "refresh_token": refresh_token}
        params = {}

        if options:
            if options.get("flags"):
                flags_str = helpers.format_flag_query(options["flags"])
                params["flags"] = flags_str

        response = helpers.requester(
            method, url, data=data, auth=self.auth, params=params
        )
        data = response.json()
        return types.make_access_object(_set_expiration(data))


# Static helpers for AuthClient


def _set_expiration(access: dict) -> dict:
    expire_date = datetime.utcnow() + timedelta(seconds=access["expires_in"])
    refresh_expire_date = datetime.utcnow() + timedelta(days=60)
    access["expiration"] = expire_date
    access["refresh_expiration"] = refresh_expire_date
    return access
