import unittest
import responses
import smartcar
import base64
import time
from datetime import datetime, timedelta
from urllib.parse import urlencode, parse_qs, urlparse


def assertDeepEquals(self, dict1, dict2):
    self.assertEqual(len(dict2), len(dict1))

    for param in dict1:
        self.assertEqual(dict2[param], dict1[param])


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
        self.scope = ['a', 'b', 'c']
        self.client = smartcar.AuthClient(
            self.client_id, self.client_secret, self.redirect_uri, True
        )
        self.maxDiff = None
        self.basic_auth = basic_auth(self.client_id, self.client_secret)
        self.expected = {"key": "value", "expires_in": 7200}

    def test_is_expired(self):
        access = {"expires_in": 7200}

        now = datetime.utcnow()
        two_hours_from_now = datetime.utcnow() + timedelta(hours=2.5)

        access["expiration"] = datetime.utcnow() + timedelta(
            seconds=access["expires_in"]
        )
        self.assertTrue(now <= access["expiration"] < two_hours_from_now)

        self.assertFalse(smartcar.is_expired(access["expiration"]))

        access["expiration"] = datetime.utcnow() - timedelta(hours=2.1)

        self.assertTrue(smartcar.is_expired(access["expiration"]))

    def test_get_auth_url(self):
        client = smartcar.AuthClient(
            self.client_id, self.client_secret, self.redirect_uri
        )
        actual = client.get_auth_url(force=True, state="stuff")
        query = urlencode(
            {
                "response_type": "code",
                "client_id": self.client_id,
                "redirect_uri": self.redirect_uri,
                "approval_prompt": "force",
                "state": "stuff",
            }
        )
        expected = smartcar.const.CONNECT_URL + "/oauth/authorize?" + query

        expected_params = parse_qs(expected)
        actual_params = parse_qs(actual)

        assertDeepEquals(self, expected_params, actual_params)

    def test_get_auth_url_with_scope(self):
        client = smartcar.AuthClient(
            self.client_id, self.client_secret, self.redirect_uri)

        test_scope = ['a', 'b', 'c']
        actual = client.get_auth_url(
            force=True, state="stuff", scope=test_scope)
        query = urlencode(
            {
                "response_type": "code",
                "client_id": self.client_id,
                "redirect_uri": self.redirect_uri,
                "approval_prompt": "force",
                "scope": " ".join(test_scope),
                "state": "stuff",
            }
        )
        expected = smartcar.const.CONNECT_URL + "/oauth/authorize?" + query

        expected_params = parse_qs(expected)
        actual_params = parse_qs(actual)

        assertDeepEquals(self, expected_params, actual_params)

    def test_get_auth_url_test_mode_true(self):
        client = smartcar.AuthClient(
            self.client_id,
            self.client_secret,
            self.redirect_uri,
            test_mode=True,
        )
        actual = client.get_auth_url(force=True, state="stuff")
        query = urlencode(
            {
                "response_type": "code",
                "client_id": self.client_id,
                "redirect_uri": self.redirect_uri,
                "approval_prompt": "force",
                "mode": "test",
                "state": "stuff",
            }
        )
        expected = smartcar.const.CONNECT_URL + "/oauth/authorize?" + query

        expected_params = parse_qs(expected)
        actual_params = parse_qs(actual)

        assertDeepEquals(self, expected_params, actual_params)

    def test_get_auth_url_test_mode_no_keyword_true(self):
        client = smartcar.AuthClient(
            self.client_id, self.client_secret, self.redirect_uri,  True
        )
        actual = client.get_auth_url(force=True, state="stuff")
        query = urlencode(
            {
                "response_type": "code",
                "client_id": self.client_id,
                "redirect_uri": self.redirect_uri,
                "approval_prompt": "force",
                "mode": "test",
                "state": "stuff",
            }
        )
        expected = smartcar.const.CONNECT_URL + "/oauth/authorize?" + query

        expected_params = parse_qs(expected)
        actual_params = parse_qs(actual)

        assertDeepEquals(self, expected_params, actual_params)

    def test_get_auth_url_test_mode_false(self):
        client = smartcar.AuthClient(
            self.client_id,
            self.client_secret,
            self.redirect_uri,
            test_mode=False,
        )
        actual = client.get_auth_url(force=True, state="stuff")
        query = urlencode(
            {
                "response_type": "code",
                "client_id": self.client_id,
                "redirect_uri": self.redirect_uri,
                "approval_prompt": "force",
                "state": "stuff",
            }
        )
        expected = smartcar.const.CONNECT_URL + "/oauth/authorize?" + query

        expected_params = parse_qs(expected)
        actual_params = parse_qs(actual)

        assertDeepEquals(self, expected_params, actual_params)

    def test_get_auth_url_make_bypass(self):
        test_bypass = "BMW"

        client = smartcar.AuthClient(
            self.client_id,
            self.client_secret,
            self.redirect_uri
        )

        actual = client.get_auth_url(
            force=True, state="stuff", make_bypass=test_bypass)
        actual_query = urlparse(actual).query
        expected_query = urlencode(
            {
                "response_type": "code",
                "client_id": self.client_id,
                "redirect_uri": self.redirect_uri,
                "approval_prompt": "force",
                "state": "stuff",
                "make": "BMW",
            }
        )

        expected_params = parse_qs(expected_query)
        actual_params = parse_qs(actual_query)

        assertDeepEquals(self, expected_params, actual_params)

    def test_get_auth_url_single_select_bool(self):
        client = smartcar.AuthClient(
            self.client_id,
            self.client_secret,
            self.redirect_uri,
        )

        actual = client.get_auth_url(
            force=True, state="stuff", single_select=True)

        actual_query = urlparse(actual).query
        expected_query = urlencode(
            {
                "response_type": "code",
                "client_id": self.client_id,
                "redirect_uri": self.redirect_uri,
                "approval_prompt": "force",
                "state": "stuff",
                "single_select": True,
            }
        )

        expected_params = parse_qs(expected_query)
        actual_params = parse_qs(actual_query)

        assertDeepEquals(self, expected_params, actual_params)

    def test_get_auth_url_single_select_dictionary_vin(self):
        single_select = {"vin": "12345678901234"}

        client = smartcar.AuthClient(
            self.client_id,
            self.client_secret,
            self.redirect_uri,
        )

        actual = client.get_auth_url(
            force=True, state="stuff", single_select=single_select
        )

        query = urlencode(
            {
                "response_type": "code",
                "client_id": self.client_id,
                "redirect_uri": self.redirect_uri,
                "approval_prompt": "force",
                "state": "stuff",
                "state": "stuff",
                "single_select_vin": "12345678901234",
                "single_select": True,
            }
        )

        expected_params = parse_qs(query)
        actual_params = parse_qs(urlparse(actual).query)

        assertDeepEquals(self, expected_params, actual_params)

    def test_get_auth_url_single_select_junk_values(self):
        client = smartcar.AuthClient(
            self.client_id,
            self.client_secret,
            self.redirect_uri,
        )

        actual = client.get_auth_url(
            force=True, state="stuff", single_select="potato")

        query = urlencode(
            {
                "response_type": "code",
                "client_id": self.client_id,
                "redirect_uri": self.redirect_uri,
                "approval_prompt": "force",
                "state": "stuff",
                "single_select": False,
            }
        )

        expected = smartcar.const.CONNECT_URL + "/oauth/authorize?" + query

        expected_params = parse_qs(query)
        actual_params = parse_qs(query)

        assertDeepEquals(self, expected_params, actual_params)

    def test_get_auth_url_single_select_junk_keys(self):
        info = {"pizza": "TESLA"}

        client = smartcar.AuthClient(
            self.client_id,
            self.client_secret,
            self.redirect_uri,
        )

        actual = client.get_auth_url(
            force=True, state="stuff", single_select="potato")

        actual_query = urlparse(actual).query
        expected_query = urlencode(
            {
                "response_type": "code",
                "client_id": self.client_id,
                "redirect_uri": self.redirect_uri,
                "approval_prompt": "force",
                "state": "stuff",
                "single_select": False,
            }
        )

        expected_params = parse_qs(expected_query)
        actual_params = parse_qs(actual_query)

        assertDeepEquals(self, expected_params, actual_params)

    def test_get_auth_url_flags_country(self):
        client = smartcar.AuthClient(
            self.client_id, self.client_secret, self.redirect_uri
        )
        actual = client.get_auth_url(
            force=True, state="stuff", flags=["country:DE"])
        query = urlencode(
            {
                "response_type": "code",
                "client_id": self.client_id,
                "redirect_uri": self.redirect_uri,
                "approval_prompt": "force",
                "state": "stuff",
                "flags": "country:DE",
            }
        )
        expected = smartcar.const.CONNECT_URL + "/oauth/authorize?" + query

        expected_params = parse_qs(expected)
        actual_params = parse_qs(actual)

        assertDeepEquals(self, expected_params, actual_params)

    @responses.activate
    def test_exchange_code(self):
        body = {
            "grant_type": "authorization_code",
            "code": "code",
            "redirect_uri": self.redirect_uri,
        }
        responses.add("POST", smartcar.const.AUTH_URL, json=self.expected)
        actual = self.client.exchange_code("code")
        self.assertIn("key", actual)
        self.assertTrue(actual["expiration"] > datetime.utcnow())
        self.assertTrue(actual["refresh_expiration"] > datetime.utcnow())
        self.assertEqual(request().headers["Authorization"], self.basic_auth)
        self.assertEqual(
            request(
            ).headers["Content-Type"], "application/x-www-form-urlencoded"
        )
        self.assertEqual(request().body, urlencode(body))

    @responses.activate
    def test_exchange_token(self):
        body = {"grant_type": "refresh_token",
                "refresh_token": "refresh_token"}
        responses.add("POST", smartcar.const.AUTH_URL, json=self.expected)
        actual = self.client.exchange_refresh_token("refresh_token")
        self.assertIn("key", actual)
        self.assertTrue(actual["expiration"] > datetime.utcnow())
        self.assertTrue(actual["refresh_expiration"] > datetime.utcnow())
        self.assertEqual(request().headers["Authorization"], self.basic_auth)
        self.assertEqual(
            request(
            ).headers["Content-Type"], "application/x-www-form-urlencoded"
        )
        self.assertEqual(request().body, urlencode(body))

    @responses.activate
    def test_is_compatible(self):
        fake_vin = "vin"
        scope = ["read_odometer", "read_location"]

        query = {
            "vin": fake_vin,
            "scope": "read_odometer read_location",
            "country": "US",
        }
        responses.add(
            "GET",
            smartcar.const.API_URL + "/v1.0/compatibility?" + urlencode(query),
            json={"compatible": True},
            match_querystring=True,
        )
        actual = self.client.is_compatible(fake_vin, scope)
        self.assertTrue(actual)

    @responses.activate
    def test_is_compatible_select_country(self):
        fake_vin = "vin"
        country = "DE"
        scope = ["read_odometer", "read_location"]

        query = {
            "vin": fake_vin,
            "scope": "read_odometer read_location",
            "country": country,
        }
        responses.add(
            "GET",
            smartcar.const.API_URL + "/v1.0" +
            "/compatibility?" + urlencode(query),
            json={"compatible": True},
            match_querystring=True,
        )
        actual = self.client.is_compatible(fake_vin, scope, country)
        self.assertTrue(actual)

    @responses.activate
    def test_get_vehicle_ids(self):
        query = {"limit": 11, "offset": 1}
        access_token = "access_token"
        url = smartcar.const.API_URL + "/v1.0/vehicles?" + urlencode(query)
        responses.add("GET", url, json=self.expected, match_querystring=True)
        actual = smartcar.get_vehicle_ids(
            access_token, limit=query["limit"], offset=query["offset"]
        )
        self.assertEqual(actual, self.expected)
        self.assertEqual(
            request().headers["Authorization"], "Bearer " + access_token)

    @responses.activate
    def test_get_user_id(self):
        access_token = "access_token"
        data = {
            "id": "user_id",
        }
        url = smartcar.const.API_URL + "/v1.0" + "/user"
        responses.add("GET", url, json=data)
        actual = smartcar.get_user_id(access_token)
        self.assertEqual(actual, data["id"])
        self.assertEqual(
            request().headers["Authorization"], "Bearer " + access_token)

    @responses.activate
    def test_set_api_version(self):
        access_token = "access_token"
        data = {
            "id": "user_id",
        }
        url = smartcar.const.API_URL + "/v2.0" + "/user"
        responses.add("GET", url, json=data)
        smartcar.set_api_version("2.0")

        actual = smartcar.get_user_id(access_token)
        self.assertEqual(actual, data["id"])
        self.assertEqual(
            request().headers["Authorization"], "Bearer " + access_token)
        smartcar.set_api_version("1.0")

    @responses.activate
    def test_v2_exception(self):
        access_token = "access_token"
        error = """{
            "type": "TYPE",
            "statusCode": 404,
            "code": "CODE",
            "description": "DESCRIPTION",
            "docURL": null,
            "requestId": "",
            "resolution": null,
            "detail": null
        }"""
        url = smartcar.const.API_URL + "/v2.0" + "/user"
        responses.add(
            "GET",
            url,
            body=error,
            status=404,
            headers={"Content-Type": "application/json"},
        )
        smartcar.set_api_version("2.0")

        try:
            actual = smartcar.get_user_id(access_token)
        except smartcar.exceptions.SmartcarExceptionV2 as err:
            self.assertEqual(err.type, "TYPE")
            self.assertEqual(err.code, "CODE")
            self.assertEqual(err.description, "DESCRIPTION")
            self.assertEqual(err.doc_url, None)
            self.assertEqual(err.resolution, None)
            self.assertEqual(err.detail, None)
            self.assertEqual(str(err), "TYPE:CODE - DESCRIPTION")
        finally:
            smartcar.set_api_version("1.0")

    @responses.activate
    def test_v2_exception_string_response(self):
        access_token = "access_token"
        error = "This error is just a message"
        url = smartcar.const.API_URL + "/v2.0" + "/user"
        responses.add(
            "GET", url, body=error, status=404, headers={"Content-Type": "text/html"}
        )
        smartcar.set_api_version("2.0")

        try:
            actual = smartcar.get_user_id(access_token)
        except smartcar.exceptions.SmartcarExceptionV2 as err:
            self.assertEqual(err.description, error)
            self.assertEqual(str(err), error)
        finally:
            smartcar.set_api_version("1.0")
