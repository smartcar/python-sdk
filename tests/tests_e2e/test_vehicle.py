import smartcar
from test_base import TestBase
import unittest

# tests run in alphabetical order by default, however, we want
# to run disconnect() last so we don't have to reauth again
# the lambda function below sorts it in reverse alphabetical order
unittest.TestLoader.sortTestMethodsUsing = lambda _, x, y: (y > x) - (y < x)


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

    def test_location(self):
        location = self.vehicle.location()
        self.assertIsNotNone(location)

    def test_info(self):
        info = self.vehicle.info()
        self.assertIsNotNone(info)

    def test_permissions(self):
        permissions = self.vehicle.permissions()
        self.assertIsNotNone(permissions)

    def test_vin(self):
        vin = self.vehicle.vin()
        self.assertIsNotNone(vin)

    def test_lock(self):
        lock = self.vehicle.lock()
        self.assertEqual(lock["status"], "success")

    def test_unlock(self):
        unlock = self.vehicle.unlock()
        self.assertEqual(unlock["status"], "success")

    def test_disconnect(self):
        disconnected = self.vehicle.disconnect()
        self.assertIsNone(disconnected)
