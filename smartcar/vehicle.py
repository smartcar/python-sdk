import dateutil.parser
import smartcar.types as ty
from smartcar.api import Smartcar


class Vehicle(object):
    def __init__(self, vehicle_id: str, access_token: str, options: dict = None):
        """
        Initializes a new Vehicle to use for making requests to the Smartcar API.

        Args:
            vehicle_id (str): the vehicle's unique identifier
            access_token (str): a valid access token
            options (dict, optional): Can contain the following keys:
                unit_system (str, optional): the unit system to use for vehicle data.
                    Defaults to metric.
        """
        self.vehicle_id = vehicle_id
        self.access_token = access_token
        self.api = Smartcar(access_token, vehicle_id=vehicle_id)

        if options:
            if options.get('unit_system'):
                self.set_unit_system(options['unit_system'])

    def set_unit_system(self, unit_system):
        """
        Update the unit system to use in requests to the Smartcar API.

        Args:
            unit_system (str): the unit system to use (metric/imperial)
        """
        if unit_system not in ("metric", "imperial"):
            raise ValueError("unit must be either metric or imperial")
        else:
            self.api.set_unit_system(unit_system)

    def vin(self) -> str:
        """
        GET Vehicle.vin

        Returns:
            str: vehicle's vin

        Raises:
            SmartcarException
        """
        response = self.api.get("vin")
        return response.json()["vin"]

    def charge(self) -> ty.Charge:
        """
        GET Vehicle.charge

        Returns:
            Charge: NamedTuple("Charge", [("is_plugged_in", bool), ("status", str), ("meta", Meta)])

        Raises:
            SmartcarException
        """
        response = self.api.get("charge")
        data = response.json()
        result = ty.Charge(data['isPluggedIn'], data['state'], ty.Meta(**response.headers))
        return result

    def battery(self) -> ty.Battery:
        """
        GET Vehicle.battery

        Returns:
            Battery: NamedTuple("Battery", [("percent_remaining", float), ("range", float), ("meta", Meta)])

        Raises:
            SmartcarException
        """
        response = self.api.get("battery")
        data = response.json()
        result = ty.Battery(data['percentRemaining'], data['range'], ty.Meta(**response.headers))
        return result

    def battery_capacity(self) -> ty.BatteryCapacity:
        """
        GET Vehicle.battery_capacity

        Returns:
            BatteryCapacity: NamedTuple("BatteryCapacity", [("capacity", float), ("meta", Meta)])

        Raises:
            SmartcarException
        """
        response = self.api.get("battery/capacity")
        data = response.json()
        result = ty.BatteryCapacity(data['capacity'], ty.Meta(**response.headers))
        return result

    def fuel(self) -> ty.Fuel:
        """
        GET Vehicle.fuel

        Returns:
            Fuel: NamedTuple("Fuel", [("range", float),
                ("percentRemaining", float), ("amountRemaining", float), ("meta", Meta)])

        Raises:
            SmartcarException
        """
        response = self.api.get("fuel")
        data = response.json()
        result = ty.Fuel(data['range'], data['percentRemaining'], data['amountRemaining'], ty.Meta(**response.headers))
        return result

    def tire_pressure(self):
        """
        GET Vehicle.tire_pressure

        Returns:
            dict: vehicle's tire pressure status

        Raises:
            SmartcarException
        """
        response = self.api.get("tires/pressure")
        data = response.json()
        result = ty.TirePressure(data['frontLeft'], data['frontRight'], data['backLeft'], data['backRight'],
                                 ty.Meta(**response.headers))
        return result

    def oil(self) -> ty.Oil:
        """
        GET Vehicle.oil

        Returns:
            Oil: NamedTuple("Oil", [("life_remaining", float), ("meta", Meta)])

        Raises:
            SmartcarException
        """
        response = self.api.get("engine/oil")
        data = response.json()
        result = ty.Oil(data['lifeRemaining'], ty.Meta(**response.headers))
        return result

    def odometer(self) -> ty.Odometer:
        """
        GET Vehicle.odometer

        Returns:
            Odometer: NamedTuple("Odometer", [("distance", float), ("meta", Meta)])

        Raises:
            SmartcarException
        """
        response = self.api.get("odometer")
        data = response.json()
        result = ty.Odometer(data["distance"], ty.Meta(**response.headers))
        return result

    def location(self) -> ty.Location:
        """
        GET Vehicle.location

        Returns:
            Location: NamedTuple("Location", [("latitude", float), ("longitude", float), ("meta", Meta)])

        Raises:
            SmartcarException
        """
        response = self.api.get("location")
        data = response.json()
        result = ty.Location(data["latitude"], data["longitude"], ty.Meta(**response.headers))
        return result

    def info(self) -> ty.Info:
        """
        GET Vehicle.info

        Returns:
            Info: NamedTuple("Info", [("id", str), ("make", str), ("model", str), ("year", str), ("meta", Meta)])

        Raises:
            SmartcarException
        """
        response = self.api.get("")
        data = response.json()
        result = ty.Info(data["id"], data["make"], data["model"], data["year"], ty.Meta(**response.headers))
        return result

    def lock(self) -> ty.Status:
        """
        POST Vehicle.lock

        Returns:
            Status: NamedTuple("Status", [("status", str), ("meta", Meta)])

        Raises:
            SmartcarException
        """
        response = self.api.action("security", "LOCK")
        data = response.json()
        result = ty.Status(data['status'], ty.Meta(**response.headers))
        return result

    def unlock(self) -> ty.Status:
        """
        POST Vehicle.unlock

        Returns:
            Status: NamedTuple("Status", [("status", str), ("meta", Meta)])

        Raises:
            SmartcarException
        """
        response = self.api.action("security", "UNLOCK")
        data = response.json()
        result = ty.Status(data['status'], ty.Meta(**response.headers))
        return result

    def start_charge(self) -> ty.Status:
        """
        POST Vehicle.start_charge

        Returns:
            Status: NamedTuple("Status", [("status", str), ("meta", Meta)])

        Raises:
            SmartcarException
        """
        response = self.api.action("charge", "START")
        data = response.json()
        result = ty.Status(data['status'], ty.Meta(**response.headers))
        return result

    def stop_charge(self) -> ty.Status:
        """
        POST Vehicle.stop_charge

        Returns:
            Status: NamedTuple("Status", [("status", str), ("meta", Meta)])

        Raises:
            SmartcarException
        """
        response = self.api.action("charge", "STOP")
        data = response.json()
        result = ty.Status(data['status'], ty.Meta(**response.headers))
        return result

    def batch(self, paths):
        """
        POST Vehicle.batch

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
            requests.append({"path": path})
        response = self.api.batch(requests)
        batch_dict = dict()
        for response in response.json()["responses"]:
            path = response["path"]
            batch_dict[path] = {
                "code": response["code"],
                "headers": response["headers"],
                "body": response["body"],
            }
        return batch_dict

    def permissions(self):
        """
        GET Vehicle.permissions

        Returns:
            list: vehicle's permissions

        Raises:
            SmartcarException
        """
        response = self.api.permissions()
        return response.json()["permissions"]

    def disconnect(self) -> ty.Status:
        """
        Disconnect this vehicle from the connected application.

        Note: Calling this method will invalidate your access token and you will
        have to have the user reauthorize the vehicle to your application if you
        wish to make requests to it

        Returns:
            Status: NamedTuple("Status", [("status", str), ("meta", Meta)])

        Raises:
            SmartcarException
        """
        response = self.api.disconnect()
        data = response.json()
        result = ty.Status(data['status'], ty.Meta(**response.headers))
        return result
