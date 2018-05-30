from smartcar import api
import unittest

class TestAPI(unittest.TestCase):
    def test_format_default(self):
        a = api.Api('db848eec-6395-11e8-8b72-3b60222a171d', 'fc93a23a-6395-11e8-808d-7b9ff2b247b1')
        url = a._format('odometer')
        self.assertEqual(url, 'https://api.smartcar.com/v1.0/vehicles/fc93a23a-6395-11e8-808d-7b9ff2b247b1/odometer')
