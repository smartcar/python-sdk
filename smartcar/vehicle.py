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
        self.api.set_unit_system(
            'metric' if unit_system == 'metric' else 'imperial')

    def set_unit_system(self, unit_system):
        """ Update the unit system to use in requests to the Smartcar API.

        Args:
            unit_system (str): the unit system to use (metric/imperial)

        """
        if unit_system not in ('metric', 'imperial'):
            raise ValueError("unit must be either metric or imperial")
        else:
            self.api.set_unit_system(unit_system)

    def info(self):
        """ GET Vehicle.info

        Returns:
            dict: vehicle's info

        Raises:
            SmartcarException

        """
        response = self.api.get('')

        return response.json()

    def vin(self):
        """ GET Vehicle.vin

        Returns:
            str: vehicle's vin

        Raises:
            SmartcarException

        """
        response = self.api.get('vin')

        return response.json()['vin']

    def permissions(self):
        """ GET Vehicle.permissions

        Returns:
            list: vehicle's permissions

        Raises:
            SmartcarException

        """
        response = self.api.permissions()

        return response.json()['permissions']

    def has_permissions(self, permissions):
      """ Checks if vehicle has specified permission(s).

        Args:
            permissions (str or list of str): Permission(s) to check

        Returns:
            boolean: Whether the vehicle has the specified permission(s)
      """
      vehicle_permissions = self.permissions()
      prefix = "required:"

      if isinstance(permissions, list):
        contained = [permission.replace(prefix, '', 1) in vehicle_permissions for permission in permissions]

        if False in contained:
          return False
        else:
          return True
      else:
        return permissions.replace(prefix, '', 1) in vehicle_permissions

    def disconnect(self):
        """ Disconnect this vehicle from the connected application.

        Note: Calling this method will invalidate your access token and you will
        have to have the user reauthorize the vehicle to your application if you
        wish to make requests to it

        Raises:
            SmartcarException

        """
        self.api.disconnect()

    def odometer(self):
        """ GET Vehicle.odometer

        Returns:
            dict: vehicle's odometer

        Raises:
            SmartcarException
        """
        response = self.api.get('odometer')

        return {
            'data': response.json(),
            'unit_system': response.headers['sc-unit-system'],
            'age': dateutil.parser.parse(response.headers['sc-data-age']),
        }

    def fuel(self):
        """ GET Vehicle.fuel

        Returns:
            dict: vehicle's fuel status

        Raises:
            SmartcarException

        """
        response = self.api.get('fuel')

        return {
            'data': response.json(),
            'unit_system': response.headers['sc-unit-system'],
            'age': dateutil.parser.parse(response.headers['sc-data-age']),
        }

    def oil(self):
        """ GET Vehicle.oil

        Returns:
            dict: vehicle's oil status

        Raises:
            SmartcarException

        """
        response = self.api.get('engine/oil')

        return {
            'data': response.json(),
            'age': dateutil.parser.parse(response.headers['sc-data-age']),
        }

    def tire_pressure(self):
        """ GET Vehicle.tire_pressure

        Returns:
            dict: vehicle's tire pressure status

        Raises:
            SmartcarException

        """
        response = self.api.get('tires/pressure')

        return {
            'data': { "tires": response.json() },
            'unit_system': response.headers['sc-unit-system'],
            'age': dateutil.parser.parse(response.headers['sc-data-age']),
        }

    def battery(self):
        """ GET Vehicle.battery

        Returns:
            dict: vehicle's battery status

        Raises:
            SmartcarException

        """
        response = self.api.get('battery')

        return {
            'data': response.json(),
            'unit_system': response.headers['sc-unit-system'],
            'age': dateutil.parser.parse(response.headers['sc-data-age']),
        }

    def charge(self):
        """ GET Vehicle.charge

        Returns:
            dict: vehicle's charge status

        Raises:
            SmartcarException

        """
        response = self.api.get('charge')

        return {
            'data': response.json(),
            'age': dateutil.parser.parse(response.headers['sc-data-age']),
        }

    def location(self):
        """ GET Vehicle.location

        Returns:
            dict: vehicle's location

        Raises:
            SmartcarException

        """
        response = self.api.get('location')

        return {
            'data': response.json(),
            'age': dateutil.parser.parse(response.headers['sc-data-age']),
        }

    def unlock(self):
        """ POST Vehicle.unlock

        Returns:
            array:

        Raises:
            SmartcarException

        """
        response = self.api.action('security', 'UNLOCK')
        return {
            'status': response.json()['status']
        }

    def lock(self):
        """ POST Vehicle.lock

        Returns:
            dict: status

        Raises:
            SmartcarException

        """
        response = self.api.action('security', 'LOCK')
        return {
            'status': response.json()['status']
        }

    def batch(self, paths):
        """ POST Vehicle.batch

        Args:
            paths (str[]): an array of paths to make
            the batch request to

        Returns:
            dict: the HTTP responses, keyed by path

        Raises:
            SmartcarException

        """
        requests = []
        for path in paths:
            requests.append({ 'path' : path })
        response = self.api.batch(requests)
        batch_dict = dict()
        for response in response.json()['responses']:
            path = response['path']
            batch_dict[path] = {
                'code' : response['code'],
                'headers' : response['headers'],
                'body' : response['body']
            }
        return batch_dict
