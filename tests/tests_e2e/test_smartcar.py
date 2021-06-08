import smartcar
import unittest
from auth_helpers import get_auth_client_params, run_auth_flow, DEFAULT_SCOPE


class TestSmartcarAuthE2E(unittest.TestCase):
    def test_exchange_code(self):
        client = smartcar.AuthClient(
            *get_auth_client_params())
        code = run_auth_flow(client.get_auth_url(scope=DEFAULT_SCOPE))

        def assert_access_object(access_object):
            self.assertIsNotNone(access_object)
            self.assertIn("access_token", access_object)
            self.assertIn("token_type", access_object)
            self.assertIn("refresh_token", access_object)
            self.assertIn("expires_in", access_object)
            self.assertIn("expiration", access_object)
            self.assertIn("refresh_expiration", access_object)

        access_object = client.exchange_code(code)
        assert_access_object(access_object)

        new_access_object = client.exchange_refresh_token(
            access_object["refresh_token"]
        )
        assert_access_object(new_access_object)

    def test_is_compatible(self):
        client = smartcar.AuthClient(*get_auth_client_params())

        teslaVin = "5YJXCDE22HF068739"
        audiVin = "WAUAFAFL1GN014882"

        scopes = ["read_odometer", "read_location"]

        teslaComp = client.is_compatible(teslaVin, scopes)
        audiComp = client.is_compatible(audiVin, scopes)

        self.assertTrue(teslaComp)
        self.assertFalse(audiComp)


class TestSmartcarStaticE2E(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        client = smartcar.AuthClient(*get_auth_client_params())
        code = run_auth_flow(client.get_auth_url(scope=DEFAULT_SCOPE))
        access_object = client.exchange_code(code)

        cls.access_token = access_object["access_token"]

    def test_get_vehicle_ids(self):
        vehicle_ids = smartcar.get_vehicle_ids(self.access_token)
        self.assertIsNotNone(vehicle_ids)

    def test_get_user_id(self):
        user_id = smartcar.get_user_id(self.access_token)
        self.assertIsNotNone(user_id)
