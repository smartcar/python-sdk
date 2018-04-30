import dateutil.parser
from . import exceptions as E
from . import __version__
from . import requester

class Vehicle(object):
    def __init__(self, vehicle_id, access_token, unit_system='metric'):
        self.vehicle_id = vehicle_id
        self.access_token = access_token
        self.auth = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        self.unit = 'metric' if unit_system == 'metric' else 'imperial'

    def _format(self, endpoint):
        return '{}/{}/{}'.format(const.API_URL, self.vehicle_id, endpoint)

    def _get(self, endpoint):
        url = self._format(endpoint)
        headers = self.auth
        headers[const.UNIT_HEADER] = self.unit
        return requester.call('GET', url, headers=headers)

    def _action(self, endpoint, action):
        url = self._format(endpoint)
        headers = self.auth
        headers[const.UNIT_HEADER] = self.unit
        json = { 'action': action }

        requester.call('POST', url, json=json, headers=self.auth)

    def info(self):
        response = self.get('')

        return response.json()

    def vin(self):
        response = self.get('vin')

        return response.json().vin

    def permissions(self):
        url = const.API_URL
        response = requester.call('GET', url, headers=self.auth)

        return response.json().permissions

    def disconnect(self):
        url = self._format('application')
        requester.call('DELETE', url, headers=self.auth)

    def odometer(self):
        reponse = self.get('odometer')

        return {
            data: response.json(),
            unit: self.unit,
            age: dateutil.parser.parse(response.headers['sc-data-age']),
        }

    def location(self):
        response = self.get('location')

        return {
            data: response.json(),
            age: dateutil.parser.parse(response.headers['sc-data-age']),
        }

    def unlock(self):
        self.action('security', 'UNLOCK')

    def lock(self):
        self.action('security', 'LOCK')
