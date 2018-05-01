import dateutil.parser
from .api import Api

class Vehicle(object):
    def __init__(self, vehicle_id, access_token, unit_system='metric'):
        self.vehicle_id = vehicle_id
        self.access_token = access_token
        self.api = Api(access_token, vehicle_id)
        self.api.set_unit('metric' if unit_system == 'metric' else 'imperial')

    def set_unit(self, unit):
        if unit not in ('metric','imperial'):
            raise ValueError("unit must be either metric or imperial")
        else:
            self.api.set_unit(unit)

    def info(self):
        response = self.api.get('')

        return response.json()

    def vin(self):
        response = self.api.get('vin')

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
            'unit_system': self.api.unit,
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
