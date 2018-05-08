import dateutil.parser
from .api import Api

class Vehicle(object):

    def __init__(self, vehicle_id, access_token, unit_system='metric'):
        """ Initializes a new Vehicle to use for making requests to the Smartcar API.

        Args:
            vehicle_id (str): the vehicle's unique identifier
            access_token (str): a valid access token
            unit_system (str, optional): the unit system to use for vehicle data.
                Defaults to metric.

        """
        self.vehicle_id = vehicle_id
        self.access_token = access_token
        self.api = Api(access_token, vehicle_id)
        self.api.set_unit_system('metric' if unit_system == 'metric' else 'imperial')

    def set_unit_system(self, unit_system):
        """ Update the unit system to use in requests to the Smartcar API.

        Args:
            unit_system (str): the unit system to use (metric/imperial)

        """
        if unit_system not in ('metric','imperial'):
            raise ValueError("unit must be either metric or imperial")
        else:
            self.api.set_unit_system(unit_system)

    def info(self):
        """ GET Vehicle.info

        Returns:
            dict: vehicle's info

        """
        response = self.api.get('')

        return response.json()

    def vin(self):
        """ GET Vehicle.vin

        Returns:
            str: vehicle's vin
        """
        response = self.api.get('vin')

        return response.json()['vin']

    def permissions(self):
        """ GET Vehicle.permissions

        Returns:
            list: vehicle's permissions
        """
        response = self.api.permissions()

        return response.json()['permissions']

    def disconnect(self):
        """ Disconnect this vehicle from the connected application.

        Note: Calling this method will invalidate your access token and you will
        have to have the user reauthorize the vehicle to your application if you
        wish to make requests to it

        """
        self.api.disconnect()

    def odometer(self):
        """ GET Vehicle.odometer

        Returns:
            dict: vehicle's odometer

        """
        response = self.api.get('odometer')

        return {
            'data': response.json(),
            'unit_system': response.headers['sc-unit-system'],
            'age': dateutil.parser.parse(response.headers['sc-data-age']),
        }

    def location(self):
        """ GET Vehicle.location

        Returns:
            dict: vehicle's location

        """
        response = self.api.get('location')

        return {
            'data': response.json(),
            'age': dateutil.parser.parse(response.headers['sc-data-age']),
        }

    def unlock(self):
        """ POST Vehicle.unlock

        """
        self.api.action('security', 'UNLOCK')

    def lock(self):
        """ POST Vehicle.lock

        """
        self.api.action('security', 'LOCK')
