import dateutil.parser
from .api import Api

class Vehicle(object):
    def __init__(self, vehicle_id, access_token, unit_system='metric'):
        self.vehicle_id = vehicle_id
        self.access_token = access_token
        self.api = Api(access_token, vehicle_id)
        self.api.set_unit('imperial' if unit_system else 'metric')
        self.unit = 'metric' if unit_system == 'metric' else 'imperial'

    def info(self):
        response = self.api.get('')

        return response.json()

    def vin(self):
        response = self.api.get('vin')

        print(response.json())

        return response.json()['vin']

    def permissions(self):
        response = self.api.permissions()
        return response.json()['permissions']

    def disconnect(self):
        self.api.disconnect()

    def odometer(self):
        response = self.api.get('odometer')

        return {
            'data': response.json(),
            'unit': self.unit,
            'age': dateutil.parser.parse(response.headers['sc-data-age']),
        }

    def location(self):
        response = self.api.get('location')

        return {
            'data': response.json(),
            'age': dateutil.parser.parse(response.headers['sc-data-age']),
        }

    def unlock(self):
        self.api.action('security', 'UNLOCK')

    def lock(self):
        self.api.action('security', 'LOCK')
