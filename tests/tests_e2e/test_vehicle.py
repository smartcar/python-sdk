import smartcar
from test_base import TestBase
import unittest


class TestVehicleE2E(TestBase):

    @classmethod
    def setUpClass(cls):
        super(TestVehicleE2E, cls).setUpClass()

        access_object = cls.client.exchange_code(cls.code)

        access_token = access_object['access_token']
        vehicle_ids = smartcar.get_vehicle_ids(access_token)
        cls.vehicle = smartcar.Vehicle(
            vehicle_ids['vehicles'][0],
            access_token)

    def test_odometer(self):
        odometer = self.vehicle.odometer()
        self.assertIsNotNone(odometer)

    def test_fuel(self):
        try:
            self.vehicle.fuel()
        except smartcar.PermissionException as err:
            self.assertEqual(err.message, 'Insufficient permissions to access requested resource.')

    def test_battery(self):
        battery = self.vehicle.battery()
        self.assertIsNotNone(battery)

    def test_charge(self):
        charge = self.vehicle.charge()
        self.assertIsNotNone(charge)

    def test_location(self):
        location = self.vehicle.location()
        self.assertIsNotNone(location)

    def test_info(self):
        info = self.vehicle.info()
        self.assertIsNotNone(info)

    def test_permissions(self):
        permissions = self.vehicle.permissions()
        self.assertIsNotNone(permissions)

    def test_has_permissions(self):
        single_response = self.vehicle.has_permissions("required:read_odometer")
        multi_response = self.vehicle.has_permissions(["read_odometer", "required:read_vehicle_info"])
        false_response = self.vehicle.has_permissions("read_ignition")
        false_multi_response = self.vehicle.has_permissions(["read_odometer", "read_ignition"])

        self.assertTrue(single_response)
        self.assertTrue(multi_response)
        self.assertFalse(false_response)
        self.assertFalse(false_multi_response)

    def test_vin(self):
        vin = self.vehicle.vin()
        self.assertIsNotNone(vin)

    def test_lock(self):
        lock = self.vehicle.lock()
        self.assertEqual(lock["status"], "success")

    def test_unlock(self):
        unlock = self.vehicle.unlock()
        self.assertEqual(unlock["status"], "success")


class TestVehicleDisconnectE2E(TestBase):

    @classmethod
    def setUpClass(cls):
        super(TestVehicleDisconnectE2E, cls).setUpClass()

        access_object = cls.client.exchange_code(cls.code)

        access_token = access_object['access_token']
        vehicle_ids = smartcar.get_vehicle_ids(access_token)
        cls.vehicle = smartcar.Vehicle(
            vehicle_ids['vehicles'][0],
            access_token)

    def test_disconnect(self):
        disconnected = self.vehicle.disconnect()
        self.assertIsNone(disconnected)
