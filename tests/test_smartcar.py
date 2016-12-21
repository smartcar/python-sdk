import unittest
import responses
import smartcar
import base64
import time
from datetime import datetime, timedelta
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

def basic_auth(id, secret):
    auth_pair = id + ":" + secret
    return "Basic {}".format(
        base64.b64encode(auth_pair.encode("utf-8")).decode("utf-8")
    )
def request():
    return responses.calls[0].request

class TestSmartcar(unittest.TestCase):
    def setUp(self):
        self.client_id = "client-id"
        self.client_secret = "client-secret"
        self.redirect_uri = "https://redirect.uri"
        self.scope = ["a", "b", "c"]
        self.client = smartcar.Client(self.client_id, self.client_secret,
                self.redirect_uri, self.scope)
        self.maxDiff = None
        self.basic_auth = basic_auth(self.client_id, self.client_secret)
        self.expected = {"key": "value", "expires_in":7200}

    def test_expired(self):
        access = {"expires_in": 7200}

        now = datetime.utcnow().isoformat()
        two_hours_from_now = (datetime.utcnow() + timedelta(hours=2.5)).isoformat()

        access = smartcar.set_expiration(access)
        self.assertTrue(now <= access["expiration"] < two_hours_from_now)

        self.assertFalse(smartcar.expired(access["expiration"]))

        access["expiration"] = (datetime.utcnow() - timedelta(hours=2.1)).isoformat()

        self.assertTrue(smartcar.expired(access["expiration"]))



    def test_get_auth_url(self):
        oem = "audi"
        actual = self.client.get_auth_url(oem, force=True, state="stuff")
        query = urlencode({
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": " ".join(self.scope),
            "approval_prompt": "force",
            "state": "stuff"
        })
        expected = smartcar.const.OEMS.get(oem) + "/oauth/authorize?" + query
        self.assertEqual(actual, expected)

    def test_auth_url_bad_oem(self):
        with self.assertRaises(ValueError):
            actual = self.client.get_auth_url("oem")

    @responses.activate
    def test_exchange_code(self):
        body = {
            "grant_type": "authorization_code",
            "code": "code",
            "redirect_uri": self.redirect_uri
        }
        responses.add("POST", smartcar.const.AUTH_URL, json=self.expected)
        actual = self.client.exchange_code("code")
        self.assertIn("key", actual)
        self.assertTrue(actual["expiration"] > datetime.utcnow().isoformat())
        self.assertEqual(request().headers["Authorization"], self.basic_auth)
        self.assertEqual(request().headers["Content-Type"], "application/x-www-form-urlencoded")
        self.assertEqual(request().body, urlencode(body))

    @responses.activate
    def test_exchange_token(self):
        body = {
            "grant_type": "refresh_token",
            "refresh_token": "refresh_token"
        }
        responses.add("POST", smartcar.const.AUTH_URL, json=self.expected)
        actual = self.client.exchange_token("refresh_token")
        self.assertIn("key", actual)
        self.assertTrue(actual["expiration"] > datetime.utcnow().isoformat())
        self.assertEqual(request().headers["Authorization"], self.basic_auth)
        self.assertEqual(request().headers["Content-Type"], "application/x-www-form-urlencoded")
        self.assertEqual(request().body, urlencode(body))

    @responses.activate
    def test_get_vehicles(self):
        query = { "limit": 11, "offset": 1 }
        access_token = "access_token"
        url = smartcar.const.API_URL + "?" + urlencode(query)
        responses.add("GET", url, json=self.expected, match_querystring=True)
        actual = self.client.get_vehicles(access_token, **query)
        self.assertEqual(actual, self.expected)
        self.assertEqual(request().headers["Authorization"], "Bearer " + access_token)
