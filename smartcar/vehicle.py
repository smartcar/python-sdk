from collections import namedtuple
import json
from typing import List

import smartcar.config as config
import smartcar.helpers as helpers
import smartcar.smartcar
import smartcar.types as types
import smartcar.exception as sce


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

        Attributes:
            self.vehicle_id (str)
            self.access_token (str): Access token retrieved from Smartcar Connect
            self.api_version (str): e.g. "1.0" or "2.0"
            self.unit_system (str): Must be "metric" or "imperial" (case insensitive)
        """
        self.vehicle_id = vehicle_id
        self.access_token = access_token
        self._api_version = smartcar.smartcar.API_VERSION
        self._unit_system = "metric"

        if options:
            if options.get("unit_system"):
                self._unit_system = options["unit_system"]

            if options.get("version"):
                self._api_version = options["version"]

    def vin(self) -> types.Vin:
        """
        GET Vehicle.vin

        Returns:
            Vin: NamedTuple("Vin", [("vin", str), ("meta", namedtuple)])

        Raises:
            SmartcarException
        """
        path = "vin"
        url = self._format_url(path)
        headers = self._get_headers()
        response = helpers.requester("GET", url, headers=headers)
        return types.select_named_tuple(path, response)

    def charge(self) -> types.Charge:
        """
        GET Vehicle.charge

        Returns:
            Charge: NamedTuple("Charge", [("is_plugged_in", bool), ("state", str), ("meta", namedtuple)])

        Raises:
            SmartcarException
        """
        path = "charge"
        url = self._format_url(path)
        headers = self._get_headers()
        response = helpers.requester("GET", url, headers=headers)
        return types.select_named_tuple(path, response)

    def battery(self) -> types.Battery:
        """
        GET Vehicle.battery

        Returns:
            Battery: NamedTuple("Battery", [("percent_remaining", float),
                ("range", float),
                ("meta", namedtuple)])

        Raises:
            SmartcarException
        """
        path = "battery"
        url = self._format_url(path)
        headers = self._get_headers()
        response = helpers.requester("GET", url, headers=headers)
        return types.select_named_tuple(path, response)

    def battery_capacity(self) -> types.BatteryCapacity:
        """
        GET Vehicle.battery_capacity

        Returns:
            BatteryCapacity: NamedTuple("BatteryCapacity", [("capacity", float), ("meta", namedtuple)])

        Raises:
            SmartcarException
        """
        path = "battery/capacity"
        url = self._format_url(path)
        headers = self._get_headers()
        response = helpers.requester("GET", url, headers=headers)
        return types.select_named_tuple(path, response)

    def fuel(self) -> types.Fuel:
        """
        GET Vehicle.fuel

        Returns:
            Fuel: NamedTuple("Fuel", [("range", float),
                ("percent_remaining", float), ("amount_remaining", float), ("meta", namedtuple)])

        Raises:
            SmartcarException
        """
        path = "fuel"
        url = self._format_url(path)
        headers = self._get_headers()
        response = helpers.requester("GET", url, headers=headers)
        return types.select_named_tuple(path, response)

    def tire_pressure(self) -> types.TirePressure:
        """
        GET Vehicle.tire_pressure

        Returns:
            TirePressure: NamedTuple("tirePressure", [
                ("front_left", int), ("front_right", int), ("back_left", int), ("back_right", int),
                ("meta", rs.namedtuple)
                ])

        Raises:
            SmartcarException
        """
        path = "tires/pressure"
        url = self._format_url(path)
        headers = self._get_headers()
        response = helpers.requester("GET", url, headers=headers)
        return types.select_named_tuple(path, response)

    def engine_oil(self) -> types.EngineOil:
        """
        GET Vehicle.engine_oil

        Returns:
            EngineOil: NamedTuple("EngineOil", [("life_remaining", float), ("meta", namedtuple)])

        Raises:
            SmartcarException
        """
        path = "engine/oil"
        url = self._format_url(path)
        headers = self._get_headers()
        response = helpers.requester("GET", url, headers=headers)
        return types.select_named_tuple(path, response)

    def odometer(self) -> types.Odometer:
        """
        GET Vehicle.odometer

        Returns:
            Odometer: NamedTuple("Odometer", [("distance", float), ("meta", namedtuple)])

        Raises:
            SmartcarException
        """
        path = "odometer"
        url = self._format_url(path)
        headers = self._get_headers()
        response = helpers.requester("GET", url, headers=headers)
        return types.select_named_tuple(path, response)

    def location(self) -> types.Location:
        """
        GET Vehicle.location

        Returns:
            Location: NamedTuple("Location", [("latitude", float), ("longitude", float), ("meta", namedtuple)])

        Raises:
            SmartcarException
        """
        path = "location"
        url = self._format_url(path)
        headers = self._get_headers()
        response = helpers.requester("GET", url, headers=headers)
        return types.select_named_tuple(path, response)

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
        path = "permissions"
        url = self._format_url(path)
        headers = self._get_headers()

        if paging is None:
            response = helpers.requester("GET", url, headers=self._get_headers())
        else:
            limit = paging.get("limit", 25)
            offset = paging.get("offset", 0)
            response = helpers.requester(
                "GET", url, headers=headers, params={"limit": limit, "offset": offset}
            )

        return types.select_named_tuple(path, response)

    def attributes(self) -> types.Attributes:
        """
        GET Vehicle.attributes

        Returns:
            Attributes: NamedTuple("Attributes", [("id", str), ("make", str), ("model", str), ("year", str),
            ("meta", namedtuple)])

        Raises:
            SmartcarException
        """
        path = ""
        url = self._format_url(path)
        headers = self._get_headers()
        response = helpers.requester("GET", url, headers=headers)
        return types.select_named_tuple(path, response)

    # ===========================================
    # Action (POST) Requests
    # ===========================================

    def lock(self) -> types.Status:
        """
        POST Vehicle.lock

        Returns:
            Action: NamedTuple("Action", [("status", str), ("message", str), ("meta", rs.namedtuple)])

        Raises:
            SmartcarException
        """
        url = self._format_url("security")
        headers = self._get_headers(need_unit_system=False)
        response = helpers.requester(
            "POST", url, headers=headers, json={"action": "LOCK"}
        )
        return types.select_named_tuple("lock", response)

    def unlock(self) -> types.Status:
        """
        POST Vehicle.unlock

        Returns:
            Action: NamedTuple("Action", [("status", str), ("message", str), ("meta", rs.namedtuple)])

        Raises:
            SmartcarException
        """
        url = self._format_url("security")
        headers = self._get_headers(need_unit_system=False)
        response = helpers.requester(
            "POST", url, headers=headers, json={"action": "UNLOCK"}
        )
        return types.select_named_tuple("unlock", response)

    def start_charge(self) -> types.Status:
        """
        POST Vehicle.start_charge

        Returns:
            Action: NamedTuple("Action", [("status", str), ("message", str), ("meta", rs.namedtuple)])

        Raises:
            SmartcarException
        """
        url = self._format_url("charge")
        headers = self._get_headers(need_unit_system=False)
        response = helpers.requester(
            "POST", url, headers=headers, json={"action": "START"}
        )
        return types.select_named_tuple("start_charge", response)

    def stop_charge(self) -> types.Status:
        """
        POST Vehicle.stop_charge

        Returns:
            Action: NamedTuple("Action", [("status", str), ("message", str), ("meta", rs.namedtuple)])

        Raises:
            SmartcarException
        """
        url = self._format_url("charge")
        headers = self._get_headers(need_unit_system=False)
        response = helpers.requester(
            "POST", url, headers=headers, json={"action": "STOP"}
        )
        return types.select_named_tuple("stop_charge", response)

    def batch(self, paths: List[str]) -> namedtuple:
        """
        POST Vehicle.batch

        This method follows a series of steps:
        1. Format and send request to Smartcar API batch endpoint
        2. Store each response in a batch dictionary.
        3. Attach meta object for the high-level batch request to the dictionary
        4. Transform batch_dict into a namedtuple, and return

        Args:
            paths (str[]): an array of paths to make
            the batch request to

        Returns:
            namedtuple: the responses from Smartcar API, each attribute is a lambda
            that returns the appropriate NamedTuple OR raises a SmartcarException (if
            the request results in an error).

        Raises:
            SmartcarException
        """
        # STEP 1 - Send Request
        url = self._format_url("batch")
        headers = self._get_headers()
        json_body = {"requests": [{"path": path} for path in paths]}
        response = helpers.requester("POST", url, headers=headers, json=json_body)

        # STEP 2 - Format batch_dict
        # [KEYS] will represent the path sent in the batch.
        # The name of the key will eventually be the name of the method attached to the final return.
        # [VALUES] are lambdas that return a NamedTuple OR raises a SmartcarException, depending on the
        # success of the request.
        batch_dict = dict()
        path_responses = response.json()["responses"]
        for res_dict in path_responses:
            path, attribute = helpers.format_path_and_attribute_for_batch(
                res_dict["path"]
            )

            if res_dict.get("code") == 200:
                # attach top-level sc-request-id to res_dict
                res_dict["headers"]["sc-request-id"] = response.headers.get(
                    "sc-request-id"
                )
                # use lambda default args to avoid issues with closures
                batch_dict[
                    attribute
                ] = lambda p=path, r=res_dict: types.select_named_tuple(p, r)
            else:
                # if individual response is erroneous, attach a lambda that returns a SmartcarException
                def _attribute_raise_exception(smartcar_exception):
                    raise smartcar_exception

                code = res_dict.get("code")
                headers = response.headers
                body = json.dumps(res_dict.get("body"))
                sc_exception = sce.exception_factory(code, headers, body)
                batch_dict[
                    attribute
                ] = lambda e=sc_exception: _attribute_raise_exception(e)

        # STEP 3 - Attach Meta to batch_dict
        batch_dict["meta"] = types.build_meta(response.headers)

        # STEP 4 - Transform batch_dict into a namedtuple
        return types.generate_named_tuple(batch_dict, "batch")

    # ===========================================
    # DELETE requests
    # ===========================================

    def disconnect(self) -> types.Status:
        """
        Disconnect this vehicle from the connected application.

        Note: Calling this method will invalidate your access token and you will
        have to have the user reauthorize the vehicle to your application if you
        wish to make requests to it

        Returns:
            Status: NamedTuple("Status", [("status", str), ("meta", namedtuple)])

        Raises:
            SmartcarException
        """
        url = self._format_url("application")
        headers = self._get_headers(need_unit_system=False)
        response = helpers.requester("DELETE", url, headers=headers)
        return types.select_named_tuple("disconnect", response)

    # ===========================================
    # Webhook requests
    # ===========================================

    def subscribe(self, webhook_id: str) -> types.Subscribe:
        """
        Subscribe a vehicle to a webhook

        Args:
            webhook_id (str)

        Returns:
            Subscribe: NamedTuple("Subscribe", [("webhook_id", str"), ("vehicle_id", str), ("meta", namedtuple)
        """
        url = self._format_url(f"webhooks/{webhook_id}")
        headers = self._get_headers(need_unit_system=False)
        response = helpers.requester("POST", url, headers=headers)
        return types.select_named_tuple("subscribe", response)

    def unsubscribe(self, amt: str, webhook_id: str) -> types.Status:
        """
        Subscribe a vehicle to a webhook

        Args:
            amt(str): Application Management Token, found on Smartcar Dashboard
            webhook_id (str)

        Returns:
            Status: NamedTuple("Subscribe", [("webhook_id", str"), ("vehicle_id", str), ("meta", namedtuple)
        """
        url = self._format_url(f"webhooks/{webhook_id}")

        # Note: Authorization header is different, compared to the other methods
        headers = {"Authorization": f"Bearer {amt}"}
        response = helpers.requester("DELETE", url, headers=headers)
        return types.select_named_tuple("unsubscribe", response)

    # ===========================================
    # Utility
    # ===========================================
    def set_unit_system(self, unit_system: str) -> None:
        """
        Change unit system of this instance of smartcar.Vehicle

        Args:
            unit_system (str): Must be "metric" or "imperial",
                case insensitive.

        Returns: None
        """
        if unit_system.lower() != "metric" or unit_system.lower() != "imperial":
            raise ValueError(
                "'unit_system' must be either 'metric' or 'imperial' (case insensitive)"
            )

        else:
            self._unit_system = unit_system.lower()

    # ===========================================
    # Private methods
    # ===========================================
    def _format_url(self, path: str) -> str:
        """
        Returns (str): Base url with current API version.
        User can change api_version attribute at will.
        """
        return (
            f"{config.API_URL}/v{self._api_version}/vehicles/{self.vehicle_id}/{path}"
        )

    def _get_headers(self, need_unit_system: bool = True) -> dict:
        """
        Returns (dict): Provides 'Authorization' Header
        and (optionally) the 'sc-unit-system' header.
        Some endpoints don't require the 'sc-unit-system' header.
        """
        headers = {"Authorization": f"Bearer {self.access_token}"}

        if need_unit_system:
            headers["sc-unit-system"] = self._unit_system.lower()

        return headers
