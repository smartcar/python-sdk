import smartcar
from test_base import TestBase
import unittest


class TestSmartcarAuthE2E(TestBase):

    def test_exchange_code(self):
        def assert_access_object(access_object):
            self.assertIsNotNone(access_object)
            self.assertIn('access_token', access_object)
            self.assertIn('token_type', access_object)
            self.assertIn('refresh_token', access_object)
            self.assertIn('expires_in', access_object)
            self.assertIn('expiration', access_object)
            self.assertIn('refresh_expiration', access_object)

        access_object = self.client.exchange_code(self.code)
        assert_access_object(access_object)

        new_access_object = self.client.exchange_refresh_token(
            access_object['refresh_token'])
        assert_access_object(new_access_object)

    def test_is_compatible_with_scope(self):
        teslaVin = '5YJXCDE22HF068739'
        audiVin = 'WAUANAF40HN017169'

        scopes = ['read_odometer', 'read_location']

        teslaComp = self.client.is_compatible(teslaVin, scopes)
        audiComp = self.client.is_compatible(audiVin, scopes)

        self.assertTrue(teslaComp)
        self.assertFalse(audiComp)

class TestSmartcarStaticE2E(TestBase):

    @classmethod
    def setUpClass(cls):
        super(TestSmartcarStaticE2E, cls).setUpClass()

        access_object = cls.client.exchange_code(cls.code)

        cls.access_token = access_object['access_token']

    def test_get_vehicle_ids(self):
        vehicle_ids = smartcar.get_vehicle_ids(self.access_token)
        self.assertIsNotNone(vehicle_ids)

    def test_get_user_id(self):
        user_id = smartcar.get_user_id(self.access_token)
        self.assertIsNotNone(user_id)
