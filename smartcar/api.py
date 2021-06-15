import base64
import os

import smartcar.constants as constants
import smartcar.requester as requester
import smartcar.static as static


class Smartcar(object):
    def __init__(self, access_token, vehicle_id=None):
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
        self.set_env()

    def set_env(self, testing: bool = False) -> None:
        """
        Set self.client_id, self.client_secret, and self.client_redirect_uri
        based on provided environment variables. If testing, find env variables
        following this pattern:
        'E2E_SMARTCAR_<variable>'

        If not, find env variables following this pattern:
        'SMARTCAR_CLIENT_<variable>'

        Args:
            testing(optional): boolean - Note that testing is NOT related to
                using test_mode in Smartcar. It refers to if you are testing this package
                as a contributor. Read CONTRIBUTING.md for more details
        """
        environment = "E2E_SMARTCAR" if testing else "SMARTCAR"

        self.client_id = os.environ.get(f"{environment}_CLIENT_ID")
        self.client_secret = os.environ.get(f"{environment}_CLIENT_SECRET")
        self.client_redirect_uri = os.environ.get(f"{environment}_REDIRECT_URI")

    def set_unit_system(self, unit_system):
        """
        Update the unit system to use in requests to the Smartcar API.

        Args:
            unit_system (str): the unit system to use (metric/imperial)
        """
        self.unit_system = unit_system

    def action(self, endpoint, action, **kwargs):
        """
        Sends POST requests to Smartcar API

        Args:
            endpoint (str): the Smartcar endpoint of interest
            action (str): action to be taken
            **kwargs: information to put into the body of the request

        Returns:
            Response: response from the request to the Smartcar API
        """
        url = self._format_vehicle_endpoint(endpoint)
        headers = self.auth
        json = {"action": action}
        for k, v in kwargs.items():
            if v:
                json[k] = v

        return requester.call("POST", url, json=json, headers=headers)

    def batch(self, requests):
        """
        Sends POST requests to Smartcar API

        Args:
            requests (object[]) - an array of objects containing a 'path' key

        Returns:
            Response: response from the request to the Smartcar API
        """
        endpoint = "batch"
        url = self._format_vehicle_endpoint(endpoint)
        json = {"requests": requests}
        headers = self.auth
        headers[constants.UNIT_SYSTEM_HEADER] = self.unit_system

        return requester.call("POST", url, json=json, headers=headers)

    def compatibility(self, **params):
        url = f"{constants.API_URL}/v{static.API_VERSION}/compatibility"
        id_secret = f'{self.client_id}:{self.client_secret}'
        encoded_id_secret = id_secret.encode('ascii')
        base64_bytes = base64.b64encode(encoded_id_secret)
        base64_id_secret = base64_bytes.decode('ascii')
        headers = {'Authorization': f'Basic {base64_id_secret}'}

        return requester.call("GET", url, headers=headers, params=params)

    def get(self, endpoint):
        """
        Sends GET requests to Smartcar API

        Args:
            endpoint (str): the Smartcar endpoint of interest

        Returns:
            Response: response from the request to the Smartcar API
        """
        url = self._format_vehicle_endpoint(endpoint)
        headers = self.auth
        headers[constants.UNIT_SYSTEM_HEADER] = self.unit_system
        return requester.call("GET", url, headers=headers)

    def permissions(self, **params):
        """
        Sends a request to /permissions

        Args:
            **params: parameters for the request

        Returns:
            Response: response from the request to the Smartcar API
        """
        url = self._format_vehicle_endpoint("permissions")
        return requester.call("GET", url, headers=self.auth, params=params)

    def disconnect(self):
        """
        Sends a request to /application

        Returns:
            Response: response from the request to the Smartcar API
        """
        url = self._format_vehicle_endpoint("application")
        return requester.call("DELETE", url, headers=self.auth)

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

    def user(self):
        """
        Sends a request to /user

        Returns:
            Response: response from the request to the Smartcar API
        """
        url = f"{self.base_url}/user"
        return requester.call("GET", url, headers=self.auth)

    # PRIVATE ENDPOINTS:

    def _format_vehicle_endpoint(self, endpoint):
        """
        Generates the formatted URL to <base_url>/vehicles/<vehicle_id>/<endpoint>
        These vehicle-related endpoints are widely used to get vehicle information.

        Args:
            endpoint (str): the Smartcar vehicle endpoint of interest

        Returns:
            str: formatted url
        """
        return f"{self.base_url}/vehicles/{self.vehicle_id}/{endpoint}"
