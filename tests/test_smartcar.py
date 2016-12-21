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
        self.expected = {"key": "value"}

    def test_expired(self):
        access = {"expires_in": 7200}

        now = time.time()
        hour = 3600
        access = smartcar.set_expiration(access)

        self.assertTrue(datetime.utcnow().isoformat() < access["expiration"] < (datetime.utcnow() + timedelta(hours=2.5)).isoformat())

        access["expiration"] = datetime.utcnow() - timedelta(hours=2)

        self.assertTrue(smartcar.expired(access["expiration"]))


        # self.assertTrue(smartcar.expired({
        #     "expires_in": hour,
        #     "created_at": now - 2*hour
        # }))
        #
        # self.assertFalse(smartcar.expired({
        #     "expires_in": hour,
        #     "created_at": now
        # }))

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
        self.assertTrue(actual["created_at"] < time.time())
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
        self.assertTrue(actual["created_at"] < time.time())
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
