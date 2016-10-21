import unittest
import responses
import smartcar
import base64

def query_string(data):
    return "&".join(
        k + "=" + str(v) for k,v in data.items()
    )
def basic_auth(id, secret):
    auth_pair = id + ":" + secret
    return "Basic {}".format(
        base64.b64encode(auth_pair.encode("utf-8")).decode("utf-8")
    )
def request_auth():
    return responses.calls[0].request.headers["Authorization"]

class TestSmartcar(unittest.TestCase):
    def setUp(self):
        self.client_id = "client-id"
        self.client_secret = "client-secret"
        self.redirect_uri = "https://redirect.uri"
        self.scope = ["a", "b", "c"]
        self.client = smartcar.Smartcar(self.client_id, self.client_secret, 
                self.redirect_uri, self.scope)
        self.maxDiff = None
        self.basic_auth = basic_auth(self.client_id, self.client_secret)
        self.expected = {"key": "value"}

    def test_get_auth_url(self):
        oem = "audi"
        actual = self.client.get_auth_url(oem, force=True, state="stuff",)
        query = query_string({
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": "https%3A%2F%2Fredirect.uri",
            "scope": "+".join(self.scope),
            "approval_prompt": "force",
            "state": "stuff"
        })
        base_url = smartcar.const.OEMS.get(oem)
        expected = "{}/oauth/authorize?{}".format(base_url, query)
        self.assertEqual(actual, expected)

    def test_auth_url_bad_oem(self):
        with self.assertRaises(ValueError):
            actual = self.client.get_auth_url("oem")

    @responses.activate
    def test_exchange_code(self):
        code = "code"
        query = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": "https%3A%2F%2Fredirect.uri"
        }
        url = smartcar.const.AUTH_URL + "?" + query_string(query)
        responses.add("POST", url, json=self.expected, match_querystring=True)
        actual = self.client.exchange_code(code)
        self.assertEqual(actual, self.expected)
        self.assertEqual(request_auth(), self.basic_auth)
        
    @responses.activate
    def test_exchange_token(self):
        refresh_token = "refresh_token"
        query = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
        url = smartcar.const.AUTH_URL + "?" + query_string(query)
        responses.add("POST", url, json=self.expected, match_querystring=True)
        actual = self.client.exchange_token(refresh_token)
        self.assertEqual(actual, self.expected)
        self.assertEqual(request_auth(), self.basic_auth)

    @responses.activate
    def test_get_vehicles(self):
        query = { "limit": 11, "offset": 1 }
        access_token = "access_token"
        url = smartcar.const.API_URL + "?" + query_string(query)
        responses.add("GET", url, json=self.expected, match_querystring=True)
        actual = self.client.get_vehicles(access_token, **query)
        self.assertEqual(actual, self.expected)
        self.assertEqual(request_auth(), "Bearer " + access_token)

    def test_get_vehicle(self):
        access_token = "access_token"
        vehicle_id = "vehicle_id"
        actual = self.client.get_vehicle(access_token, vehicle_id)
        self.assertEqual(actual.access_token, access_token)
        self.assertEqual(actual.vehicle_id, vehicle_id)
