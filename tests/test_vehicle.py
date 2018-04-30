import unittest
import smartcar
import responses
import json

class TestVehicle(unittest.TestCase):
    def setUp(self):
        self.access_token = 'access_token'
        self.vehicle_id = 'vehicle_id'
        self.vehicle = smartcar.Vehicle(self.vehicle_id, self.access_token)
        self.auth = 'Bearer ' + self.access_token

    def queue(self, method, endpoint, expected={ 'key': 'value' }, query=None):
        """ queue a mock response """
        url = '/'.join((smartcar.const.API_URL, self.vehicle_id, endpoint))
        if query:
            query_string = '&'.join(
                k + '=' + str(v) for k,v in query.items()
            )
            url += '?' + query_string

        responses.add(method, url,
                json=expected, match_querystring=bool(query))

    def check(self, actual, expected={ 'key': 'value' }, **kwargs):
        """
        test that the actual response equals the expected response,
        that the 'Authorization' header is the correct bearer auth string,
        and that each key in the request body is correct.
        """

        self.assertEqual(len(responses.calls), 1)

        request = responses.calls[0].request
        request_auth = request.headers['Authorization']
        self.assertEqual(request_auth, self.auth)

        if kwargs:
            request_json = json.loads(request.body.decode('utf-8'))
            for k,v in kwargs.items():
               self.assertEqual(request_json[k], v)

    @responses.activate
    def test_unit_system(self):
        self.queue('GET', 'odometer')
        self.vehicle.odometer()
        unit = responses.calls[0].request.headers[smartcar.UNIT_HEADER]
        self.assertEqual(unit, 'metric')

        self.queue('GET', 'odometer')
        self.vehicle.set_unit('imperial')
        self.vehicle.odometer()
        unit = responses.calls[1].request.headers[smartcar.UNIT_HEADER]
        self.assertEqual(unit, 'imperial')

        self.queue('POST', 'climate')
        self.vehicle.set_unit('metric')
        self.vehicle.start_climate()
        unit = responses.calls[2].request.headers[smartcar.UNIT_HEADER]
        self.assertEqual(unit, 'metric')

    @responses.activate
    def test_permission(self):
        query = { 'limit': 11, 'offset': 1 }
        self.queue('GET', 'permissions', query=query)
        self.check(self.vehicle.permissions(**query))

    @responses.activate
    def test_info(self):
        self.queue('GET', '')
        self.check(self.vehicle.info())

    @responses.activate
    def test_location(self):
        self.queue('GET', 'location')
        self.check(self.vehicle.location())

    @responses.activate
    def test_odometer(self):
        self.queue('GET', 'odometer')
        self.check(self.vehicle.odometer())

    @responses.activate
    def test_vin(self):
        self.queue('GET', 'vin', expected={ 'vin': 'fakeVin'})

        response = self.vehicle.vin()
        self.check(response, expected={ 'vin': 'fakeVin'})
        self.assertEqual(response, 'fakeVin')

    @responses.activate
    def test_disconnect(self):
        self.queue('DELETE', 'application')
        self.check(self.vehicle.disconnect())

    @responses.activate
    def test_lock(self):
        self.queue('POST', 'security')
        self.check(self.vehicle.lock(), action='LOCK')

    @responses.activate
    def test_unlock(self):
        self.queue('POST', 'security')
        self.check(self.vehicle.unlock(), action='UNLOCK')
