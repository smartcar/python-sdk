from typing import List
import requests.structures as rs

import smartcar.api
import smartcar.auth_client
import smartcar.constants as constants
import smartcar.static as static
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
                version(str, optional): Version of Smartcar API an instance of vehicle
                    will send requests to. This will override the instance's base url attribute.
        """
        self.vehicle_id = vehicle_id
        self.access_token = access_token
        self.api = Smartcar(access_token, vehicle_id=vehicle_id)

        if options:
            if options.get("unit_system"):
                self.set_unit_system(options["unit_system"])

            if options.get("version"):
                version = options["version"]
                if version != smartcar.api.API_VERSION:
                    self.api.base_url = f"{constants.API_URL}/v{version}"

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

    def vin(self) -> ty.Vin:
        """
        GET Vehicle.vin

        Returns:
            Vin: NamedTuple("Vin", [("vin", str), ("meta", CaseInsensitiveDict)])

        Raises:
            SmartcarException
        """
        response = self.api.get("vin")
        return ty.select_named_tuple("vin", response)

    def charge(self) -> ty.Charge:
        """
        GET Vehicle.charge

        Returns:
            Charge: NamedTuple("Charge", [("is_plugged_in", bool), ("status", str), ("meta", CaseInsensitiveDict)])

        Raises:
            SmartcarException
        """
        response = self.api.get("charge")
        return ty.select_named_tuple("charge", response)

    def battery(self) -> ty.Battery:
        """
        GET Vehicle.battery

        Returns:
            Battery: NamedTuple("Battery", [("percent_remaining", float),
                ("range", float),
                ("meta", CaseInsensitiveDict)]
                )

        Raises:
            SmartcarException
        """
        response = self.api.get("battery")
        return ty.select_named_tuple("battery", response)

    def battery_capacity(self) -> ty.BatteryCapacity:
        """
        GET Vehicle.battery_capacity

        Returns:
            BatteryCapacity: NamedTuple("BatteryCapacity", [("capacity", float), ("meta", CaseInsensitiveDict)])

        Raises:
            SmartcarException
        """
        response = self.api.get("battery/capacity")
        return ty.select_named_tuple("battery/capacity", response)

    def fuel(self) -> ty.Fuel:
        """
        GET Vehicle.fuel

        Returns:
            Fuel: NamedTuple("Fuel", [("range", float),
                ("percentRemaining", float), ("amountRemaining", float), ("meta", CaseInsensitiveDict)])

        Raises:
            SmartcarException
        """
        response = self.api.get("fuel")
        return ty.select_named_tuple("fuel", response)

    def tire_pressure(self):
        """
        GET Vehicle.tire_pressure

        Returns:
            dict: vehicle's tire pressure status

        Raises:
            SmartcarException
        """
        response = self.api.get("tires/pressure")
        return ty.select_named_tuple("tires/pressure", response)

    def engine_oil(self) -> ty.EngineOil:
        """
        GET Vehicle.engine_oil

        Returns:
            EngineOil: NamedTuple("EngineOil", [("life_remaining", float), ("meta", CaseInsensitiveDict)])

        Raises:
            SmartcarException
        """
        response = self.api.get("engine/oil")
        return ty.select_named_tuple("engine/oil", response)

    def odometer(self) -> ty.Odometer:
        """
        GET Vehicle.odometer

        Returns:
            Odometer: NamedTuple("Odometer", [("distance", float), ("meta", CaseInsensitiveDict)])

        Raises:
            SmartcarException
        """
        response = self.api.get("odometer")
        return ty.select_named_tuple("odometer", response)

    def location(self) -> ty.Location:
        """
        GET Vehicle.location

        Returns:
            Location: NamedTuple("Location", [("latitude", float), ("longitude", float), ("meta", CaseInsensitiveDict)])

        Raises:
            SmartcarException
        """
        response = self.api.get("location")
        return ty.select_named_tuple("location", response)

    def permissions(self, paging: dict = None):
        """
        GET Vehicle.permissions

        Args:
            paging (dict, optional): Can contain "limit" or "offset":
                limit (int, optional): The number of permissions to return
                offset (int, optional): The index to start permission list at

        Returns:
            list: vehicle's permissions

        Raises:
            SmartcarException
        """
        if paging is None:
            response = self.api.get("permissions")

        else:
            limit = paging.get("limit", 25)
            offset = paging.get("offset", 0)
            response = self.api.get("permissions", limit=limit, offset=offset)

        return ty.select_named_tuple("permissions", response)

    def info(self) -> ty.Info:
        """
        GET Vehicle.info

        Returns:
            Info: NamedTuple("Info", [("id", str), ("make", str), ("model", str), ("year", str), ("meta", CaseInsensitiveDict)])

        Raises:
            SmartcarException
        """
        response = self.api.get("")
        return ty.select_named_tuple("", response)

    # ===========================================
    # Action (POST) Requests
    # ===========================================

    def lock(self) -> ty.Status:
        """
        POST Vehicle.lock

        Returns:
            Status: NamedTuple("Status", [("status", str), ("meta", CaseInsensitiveDict)])

        Raises:
            SmartcarException
        """
        response = self.api.post("security", action="LOCK")
        return ty.select_named_tuple("lock", response)

    def unlock(self) -> ty.Status:
        """
        POST Vehicle.unlock

        Returns:
            Status: NamedTuple("Status", [("status", str), ("meta", CaseInsensitiveDict)])

        Raises:
            SmartcarException
        """
        response = self.api.post("security", action="UNLOCK")
        return ty.select_named_tuple("unlock", response)

    def start_charge(self) -> ty.Status:
        """
        POST Vehicle.start_charge

        Returns:
            Status: NamedTuple("Status", [("status", str), ("meta", CaseInsensitiveDict)])

        Raises:
            SmartcarException
        """
        response = self.api.post("charge", action="START")
        return ty.select_named_tuple("start_charge", response)

    def stop_charge(self) -> ty.Status:
        """
        POST Vehicle.stop_charge

        Returns:
            Status: NamedTuple("Status", [("status", str), ("meta", CaseInsensitiveDict)])

        Raises:
            SmartcarException
        """
        response = self.api.post("charge", action="STOP")
        return ty.select_named_tuple("stop_charge", response)

    def batch(self, paths: List[str]):
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

        # Match formatting required of Smartcar api
        for path in paths:
            requests.append({"path": path})

        response = self.api.batch(requests)

        # Generate NamedTuple for every path requested. Store in a dictionary
        batch_dict = dict()

        for res in response.json()["responses"]:
            path = res["path"][1:] if res["path"][0] == "/" else res["path"]
            batch_dict[path] = ty.select_named_tuple(path, res)

        # Attach response headers to the dictionary, and then transform to a NamedTuple
        meta = rs.CaseInsensitiveDict(response.headers)
        batch_dict["meta"] = meta
        batch = ty.generate_named_tuple(batch_dict, "batch")

        return batch

    # ===========================================
    # DELETE requests
    # ===========================================

    def disconnect(self) -> ty.Status:
        """
        Disconnect this vehicle from the connected application.

        Note: Calling this method will invalidate your access token and you will
        have to have the user reauthorize the vehicle to your application if you
        wish to make requests to it

        Returns:
            Status: NamedTuple("Status", [("status", str), ("meta", CaseInsensitiveDict)])

        Raises:
            SmartcarException
        """
        response = self.api.delete("application")
        return ty.select_named_tuple("disconnect", response)

    # ===========================================
    # Webhook requests
    # ===========================================

    def subscribe(self, webhook_id: str) -> ty.Subscribe:
        """
        Subscribe a vehicle to a webhook

        Args:
            webhook_id (str)

        Returns:
            Subscribe: NamedTuple("Subscribe", [("webhook_id", str"), ("vehicle_id", str), ("meta", CaseInsensitiveDict)
        """
        response = self.api.post(f"webhooks/{webhook_id}")
        return ty.select_named_tuple("subscribe", response)

    def unsubscribe(self, amt: str, webhook_id: str) -> rs.CaseInsensitiveDict:
        """
        Subscribe a vehicle to a webhook

        Args:
            amt(str): Application Management Token, found on Smartcar Dashboard
            webhook_id (str)

        Returns:
            Subscribe: NamedTuple("Subscribe", [("webhook_id", str"), ("vehicle_id", str), ("meta", CaseInsensitiveDict)
        """
        response = self.api.unsubscribe_from_webhook(amt, webhook_id)
        return rs.CaseInsensitiveDict(response.headers)
