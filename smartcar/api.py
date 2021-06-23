import base64
import os

import smartcar.constants as constants
import smartcar.requester as requester
import smartcar.static as static


class Smartcar(object):
    def __init__(self, access_token: str, vehicle_id: str = None):
        """
        Initialize a new Api object to directly make requests to Smartcar.

        Args:
            access_token (str): Smartcar access token
            vehicle_id (str, optional): id of the vehicle. Defaults to None.
        """
        self.access_token = access_token
        self.vehicle_id = vehicle_id
        self.auth = {"Authorization": f"Bearer {access_token}"}
        self.unit_system = "metric"
        self.base_url = f"{constants.API_URL}/v{static.API_VERSION}"
        self.client_id = None
        self.client_secret = None
        self.client_redirect_uri = None
        self._set_env()

    # ===========================================
    # Utility Methods
    # ===========================================

    def get(self, endpoint: str, **params):
        """
        Sends GET requests to Smartcar API vehicle endpoints.

        Args:
            endpoint (str): the Smartcar endpoint of interest
            **params: information to send as query parameters

        Returns:
            Response: response from the request to the Smartcar API
        """
        url = self._format_vehicle_endpoint(endpoint)
        headers = self.auth
        headers[constants.UNIT_SYSTEM_HEADER] = self.unit_system
        return requester.call("GET", url, headers=self.auth, params=params)

    def post(self, endpoint: str, **body):
        """
        Sends POST requests to Smartcar API

        Args:
            endpoint (str): the Smartcar endpoint of interest
            **body: information to put into the body of the request

        Returns:
            Response: response from the request to the Smartcar API
        """
        url = self._format_vehicle_endpoint(endpoint)
        json = dict()

        for k, v in body.items():
            if v:
                json[k] = v

        return requester.call("POST", url, json=json, headers=self.auth)

    def delete(self, endpoint: str):
        """
        Sends DELETE Requests to Smartcar API

        Args:
            endpoint (str): the Smartcar endpoint of interest

        Returns:
            Response: response from the request to the Smartcar API
        """

        url = self._format_vehicle_endpoint(endpoint)
        return requester.call("DELETE", url, headers=self.auth)

    def set_env_custom(self, client_id: str = None, client_secret: str = None) -> None:
        """
        Set self.client_id and/or self.client_secret to custom values.

        Args:
            client_id (str)
            client_secret (str)
        """
        if client_id:
            self.client_id = client_id

        if client_secret:
            self.client_secret = client_secret

    def set_unit_system(self, unit_system: str):
        """
        Update the unit system to use in requests to the Smartcar API.

        Args:
            unit_system (str): the unit system to use (metric/imperial)
        """
        self.unit_system = unit_system

    # ===========================================
    # Methods directly related to vehicle.py
    # ===========================================

    def batch(self, requests: list):
        """
        Sends POST requests to Smartcar API

        Args:
            requests (object[]) - a list of objects containing a 'path' key

        Returns:
            Response: response from the Smartcar API
        """
        endpoint = "batch"
        url = self._format_vehicle_endpoint(endpoint)
        json = {"requests": requests}
        headers = self.auth
        headers[constants.UNIT_SYSTEM_HEADER] = self.unit_system

        return requester.call("POST", url, json=json, headers=headers)

    def unsubscribe_from_webhook(self, amt: str, webhook_id: str):
        """
        Sends DELETE request to unsubscribe vehicle from webhook.
        Uses a custom header.

        Args:
            amt(str): Application Management Token, found on Smartcar dashboard.
            webhook_id(str)

        Returns:
            Response: response from the Smartcar Api
        """
        url = self._format_vehicle_endpoint(f"webhooks/{webhook_id}")
        headers = {"Authorization": f"Bearer {amt}"}
        return requester.call("DELETE", url, headers=headers)

    # ===========================================
    # Methods directly related to static.py
    # ===========================================

    def user(self):
        """
        Sends a request to /user

        Returns:
            Response: response from the request to the Smartcar API
        """
        url = f"{self.base_url}/user"
        return requester.call("GET", url, headers=self.auth)

    def vehicles(self, **params):
        """
        Sends a request to /vehicles

        Args:
            **params: parameters for the request

        Returns:
            Response: response from the request to the Smartcar API
        """
        url = f"{self.base_url}/vehicles"
        return requester.call("GET", url, headers=self.auth, params=params)

    def compatibility(self, **params):
        url = f"{constants.API_URL}/v{static.API_VERSION}/compatibility"
        id_secret = f"{self.client_id}:{self.client_secret}"
        encoded_id_secret = id_secret.encode("ascii")
        base64_bytes = base64.b64encode(encoded_id_secret)
        base64_id_secret = base64_bytes.decode("ascii")
        headers = {"Authorization": f"Basic {base64_id_secret}"}

        if params.get("flags") is None:
            params.pop("flags")

        return requester.call("GET", url, headers=headers, params=params)

    # ===========================================
    # Private Methods
    # ===========================================

    def _format_vehicle_endpoint(self, endpoint: str):
        """
        Generates the formatted URL to <base_url>/vehicles/<vehicle_id>/<endpoint>
        These vehicle-related endpoints are widely used to get vehicle information.

        Args:
            endpoint (str): the Smartcar vehicle endpoint of interest

        Returns:
            str: formatted url
        """
        return f"{self.base_url}/vehicles/{self.vehicle_id}/{endpoint}"

    def _set_env(self, testing: bool = False) -> None:
        """
        Set self.client_id, self.client_secret, and self.client_redirect_uri
        based on provided environment variables. If testing, find env variables
        following this pattern:
        'E2E_SMARTCAR_<variable>'

        If not, find env variables following this pattern:
        'SMARTCAR_CLIENT_<variable>'

        This method not to be called by users. Contributing developers should use this
        method in their testing suite.

        Args:
            testing(optional): boolean - Note that testing is NOT related to
                using test_mode in Smartcar. It refers to if you are testing this package
                as a contributor. Read CONTRIBUTING.md for more details
        """
        environment = "E2E_SMARTCAR" if testing else "SMARTCAR"

        self.client_id = os.environ.get(f"{environment}_CLIENT_ID")
        self.client_secret = os.environ.get(f"{environment}_CLIENT_SECRET")
        self.client_redirect_uri = os.environ.get(f"{environment}_REDIRECT_URI")
