import unittest
import smartcar
import requests
import responses
import json

import dateutil.parser

class TestVehicle(unittest.TestCase):
    def setUp(self):
        self.access_token = 'access_token'
        self.vehicle_id = 'vehicle_id'
        self.vehicle = smartcar.Vehicle(self.vehicle_id, self.access_token)
        self.auth = 'Bearer ' + self.access_token

    def queue(self, method, endpoint, body=None, query=None, headers=None):
        """ queue a mock response """
        url = '/'.join((smartcar.const.API_URL, self.vehicle_id, endpoint))
        if query:
            query_string = '&'.join(
                k + '=' + str(v) for k,v in query.items()
            )
            url += '?' + query_string
        if not body:
            body = {}
        if not headers:
            headers = {}

        responses.add(method, url,
                json=body,
                match_querystring=bool(query),
                headers=headers)

    def check(self, actual, **kwargs):
        """
        test that the 'Authorization' header is the correct bearer auth string,
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
        age = '2018-04-30T22:28:52+00:00'
        self.queue('GET', 'odometer', headers={
            'sc-unit-system': 'metric',
            'sc-data-age': age,
        })
        self.vehicle.odometer()
        headers = responses.calls[0].request.headers
        unit_system = headers['sc-unit-system']
        self.assertEqual(unit_system, 'metric')

        self.queue('GET', 'odometer', headers={
            'sc-unit-system': 'imperial',
            'sc-data-age': age,
        })
        self.vehicle.set_unit_system('imperial')
        self.vehicle.odometer()
        headers = responses.calls[1].request.headers
        unit_system = headers['sc-unit-system']
        self.assertEqual(unit_system, 'imperial')

    @responses.activate
    def test_permission(self):
        data = {
            "permissions": ["read_odometer"]
        }

        self.queue('GET', 'permissions', data)
        response = self.vehicle.permissions()

        self.check(response)
        self.assertEqual(response, data['permissions'])

    @responses.activate
    def test_info(self):
        data = {
          "id": "36ab27d0-fd9d-4455-823a-ce30af709ffc",
          "make": "TESLA",
          "model": "Model S",
          "year": 2014
        }

        self.queue('GET', '', body=data)
        response = self.vehicle.info()

        self.check(response)
        self.assertEqual(response, data)

    @responses.activate
    def test_location(self):
        data = {
            'latitude': 37.4292,
            'longitude': 122.1381
        }

        age = '2018-04-30T22:28:52+00:00'
        self.queue('GET', 'location', body=data, headers={ 'sc-data-age': age })
        response = self.vehicle.location()

        self.check(response)
        self.assertEqual(response['data'], data)
        self.assertEqual(response['age'], dateutil.parser.parse(age))

    @responses.activate
    def test_odometer(self):
        data = {
            'odometer': 1234
        }

        age = '2018-04-30T22:28:52+00:00'
        self.queue('GET', 'odometer', body=data, headers={
            'sc-unit-system': 'metric',
            'sc-data-age': age,
        })
        response = self.vehicle.odometer()

        self.check(response)
        self.assertEqual(response['data'], data)
        self.assertEqual(response['unit_system'], 'metric')
        self.assertEqual(response['age'], dateutil.parser.parse(age))

    @responses.activate
    def test_vin(self):
        data = { 'vin': 'fakeVin'}
        self.queue('GET', 'vin', body=data)

        response = self.vehicle.vin()
        self.check(response)
        self.assertEqual(response, data['vin'])

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
