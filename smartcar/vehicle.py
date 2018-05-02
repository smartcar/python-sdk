import dateutil.parser
from .api import Api

class Vehicle(object):

    """ Initializes a new Vehicle to use for making requests to the Smartcar API.

    Args:
        vehicle_id (str): the vehicle's unique identifier
        access_token (str): a valid access token
        unit_system (str, optional): the unit system to use for vehicle data.
            Defaults to metric.

    """
    def __init__(self, vehicle_id, access_token, unit_system='metric'):
        self.vehicle_id = vehicle_id
        self.access_token = access_token
        self.api = Api(access_token, vehicle_id)
        self.api.set_unit('metric' if unit_system == 'metric' else 'imperial')

    """ Update the unit system to use in requests to the Smartcar API.

    Args:
        unit (str): the unit system to use (metric/imperial)

    """
    def set_unit(self, unit):
        if unit not in ('metric','imperial'):
            raise ValueError("unit must be either metric or imperial")
        else:
            self.api.set_unit(unit)

    """ GET Vehicle.info

    Returns:
        dict: vehicle's info

    """
    def info(self):
        response = self.api.get('')

        return response.json()

    """ GET Vehicle.vin

    Returns:
        str: vehicle's vin
    """
    def vin(self):
        response = self.api.get('vin')

        return response.json()['vin']

    """ GET Vehicle.permissions

    Returns:
        list: vehicle's permissions
    """
    def permissions(self):
        response = self.api.permissions()

        return response.json()['permissions']

    """ Disconnect this vehicle from the connected application.

    Note: Calling this method will invalidate your access token and you will
    have to have the user reauthorize the vehicle to your application if you
    wish to make requests to it

    """
    def disconnect(self):
        self.api.disconnect()

    """ GET Vehicle.odometer

    Returns:
        dict: vehicle's odometer

    """
    def odometer(self):
        response = self.api.get('odometer')

        return {
            'data': response.json(),
            'unit_system': self.api.unit,
            'age': dateutil.parser.parse(response.headers['sc-data-age']),
        }

    """ GET Vehicle.location

    Returns:
        dict: vehicle's location

    """
    def location(self):
        response = self.api.get('location')

        return {
            'data': response.json(),
            'age': dateutil.parser.parse(response.headers['sc-data-age']),
        }

    """ POST Vehicle.unlock

    """
    def unlock(self):
        self.api.action('security', 'UNLOCK')

    """ POST Vehicle.lock

    """
    def lock(self):
        self.api.action('security', 'LOCK')
