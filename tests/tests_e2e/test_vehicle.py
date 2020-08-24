import smartcar
import unittest
from auth_helpers import (get_auth_client_params, run_auth_flow)

def get_vehicle(brand, scope):
    client = smartcar.AuthClient(*get_auth_client_params(scope))
    code = run_auth_flow(client.get_auth_url(), brand)
    access_token = client.exchange_code(code)['access_token']
    vehicle_ids = smartcar.get_vehicle_ids(access_token)
    return smartcar.Vehicle(vehicle_ids['vehicles'][0], access_token)

class TestVehicleE2E(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.volt = get_vehicle('CHEVROLET', [
            'required:read_vehicle_info',
            'required:read_location',
            'required:read_odometer',
            'required:control_security',
            'required:read_vin',
            'required:read_fuel',
            'required:read_battery',
            'required:read_charge',
            'required:read_engine_oil',
            'required:read_tires',
        ])
        cls.egolf = get_vehicle('VOLKSWAGEN', ['required:control_charge'])

    def test_info(self):
        info = self.volt.info()
        self.assertIsNotNone(info)

    def test_vin(self):
        vin = self.volt.vin()
        self.assertIsNotNone(vin)

    def test_location(self):
        location = self.volt.location()
        self.assertIsNotNone(location)

    def test_odometer(self):
        odometer = self.volt.odometer()
        self.assertIsNotNone(odometer)

    def test_fuel(self):
        fuel = self.volt.fuel()
        self.assertIsNotNone(fuel)

    def test_oil(self):
        oil = self.volt.oil()
        self.assertIsNotNone(oil)

    def test_tire_pressure(self):
        tire_pressure = self.volt.tire_pressure()
        self.assertIsNotNone(tire_pressure)

    def test_battery(self):
        battery = self.volt.battery()
        self.assertIsNotNone(battery)

    def test_charge(self):
        charge = self.volt.charge()
        self.assertIsNotNone(charge)

    def test_lock(self):
        lock = self.volt.lock()
        self.assertEqual(lock["status"], "success")

    def test_unlock(self):
        unlock = self.volt.unlock()
        self.assertEqual(unlock["status"], "success")

    def test_start_charge(self):
        response = self.egolf.start_charge()
        self.assertEqual(response["status"], "success")

    def test_stop_charge(self):
        response = self.egolf.stop_charge()
        self.assertEqual(response["status"], "success")

    def test_batch(self):
        batch = self.volt.batch(['/odometer', '/location'])
        self.assertIsNotNone(batch)

    def test_permissions(self):
        permissions = self.volt.permissions()
        self.assertIsNotNone(permissions)

    def test_has_permissions(self):
        single_response = self.volt.has_permissions("required:read_odometer")
        multi_response = self.volt.has_permissions(["read_odometer", "required:read_vehicle_info"])
        false_response = self.volt.has_permissions("read_ignition")
        false_multi_response = self.volt.has_permissions(["read_odometer", "read_ignition"])

        self.assertTrue(single_response)
        self.assertTrue(multi_response)
        self.assertFalse(false_response)
        self.assertFalse(false_multi_response)

    def test_set_unit_system(self):
        self.volt.set_unit_system('imperial')
        batch = self.volt.batch(['/odometer', '/fuel'])
        self.assertEqual(batch['/odometer']['headers']['sc-unit-system'], 'imperial')

    ## nose runs tests in alphabetical order
    def test_zzzz_disconnect(self):
        disconnected = self.volt.disconnect()
        self.assertIsNone(disconnected)
