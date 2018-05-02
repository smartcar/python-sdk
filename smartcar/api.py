from . import const, requester

class Api(object):

    def __init__(self, access_token, vehicle_id=None):
        """ Initialize a new Api object to make directly make requests to Smartcar.

        Args:
            access_token (str): Smartcar access token
            vehicle_id (str, optional): id of the vehicle. Defaults to None.
        """
        self.access_token = access_token
        self.vehicle_id = vehicle_id
        self.auth = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        self.unit = 'metric'

    def set_unit(self, unit):
        """ Update the unit system to use in requests to the Smartcar API.

        Args:
            unit (str): the unit system to use (metric/imperial)

        """
        self.unit = unit

    def _format(self, endpoint):
        """ Generates the formated URL

        Args:
            endpoint (str): the Smartcar endpoint of interest

        Returns:
            str: formatted url

        """
        return '{}/{}/{}'.format(const.API_URL, self.vehicle_id, endpoint)

    def action(self, endpoint, action, **kwargs):
        """ Sends POST requests to Smartcar API

        Args:
            endpoint (str): the Smartcar endpoint of interest
            action (str): action to be taken
            **kwargs: information to put into the body of the request

        Returns:
            Response: response from the request to the Smartcar API

        """
        url = self._format(endpoint)
        headers = self.auth
        headers[const.UNIT_HEADER] = self.unit
        json = { 'action': action }
        for k,v in kwargs.items():
            if v:
                json[k] = v

        return requester.call('POST', url, json=json, headers=self.auth)

    def get(self, endpoint):
        """ Sends GET requests to Smartcar API

        Args:
            endpoint (str): the Smartcar endpoint of interest

        Returns:
            Response: response from the request to the Smartcar API

        """
        url = self._format(endpoint)
        headers = self.auth
        headers[const.UNIT_HEADER] = self.unit
        return requester.call('GET', url, headers=headers)

    def permissions(self, **params):
        """ Sends a request to /permissions

        Args:
            **params: parameters for the request

        Returns:
            Reponse: response from the request to the Smartcar API

        """
        url = self._format('permissions')
        return requester.call('GET', url, headers=self.auth, params=params)

    def disconnect(self):
        """ Sends a request to /application

        Returns:
            Response: response from the request to the Smartcar API

        """
        url = self._format('application')
        return requester.call('DELETE', url, headers=self.auth)

    def vehicles(self, **params):
        """ Sends a request to /vehicles

        Args:
            **params: parameters for the request

        Returns:
            Response: response from the request to the Smartcar API

        """
        url = '{}/{}'.format(const.API_URL, 'vehicles')
        return requester.call('GET', url, headers=self.auth, params=params)

    def user(self, **params):
        """ Sends a request to /user

        Args:
            **params: parameters for the request

        Returns:
            Response: response from the request to the Smartcar API

        """
        url = '{}/{}'.format(const.API_URL, 'user')
        return requester.call('GET', url, headers=self.auth, params=params)
