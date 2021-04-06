import unittest
import responses
import requests
import smartcar


class TestRequester(unittest.TestCase):
    EXPECTED = "expected"
    URL = "http://fake.url"

    def queue(self, status_code, **kwargs):
        """ queue up a fake response with the specified status code """
        if not kwargs:
            json = {"message": self.EXPECTED}
        else:
            json = kwargs

        responses.add("GET", self.URL, status=status_code, json=json)

    def check(self, exception):

        self.assertRaisesRegexp(
            exception, self.EXPECTED, smartcar.requester.call, "GET", self.URL
        )

    @responses.activate
    def test_user_agent(self):
        self.queue(200)
        smartcar.requester.call("GET", self.URL)
        self.assertRegexpMatches(
            responses.calls[0].request.headers["User-Agent"],
            r"^Smartcar\/semantic-release \((\w+); (\w+)\) Python v(\d+\.\d+\.\d+)$",
        )

    @responses.activate
    def test_oauth_error(self):
        self.queue(401, error_description="unauthorized")
        try:
            smartcar.requester.call("GET", self.URL)
        except smartcar.AuthenticationException as err:
            self.assertEqual(err.message, "unauthorized")

    @responses.activate
    def test_unknown_error(self):
        self.queue(401, unknown_field="unknown error")
        try:
            smartcar.requester.call("GET", self.URL)
        except smartcar.AuthenticationException as err:
            self.assertEqual(err.message, "Unknown error")

    @responses.activate
    def test_400(self):
        self.queue(400)
        self.check(smartcar.ValidationException)

    @responses.activate
    def test_401(self):
        self.queue(401)
        self.check(smartcar.AuthenticationException)

    @responses.activate
    def test_403(self):
        self.queue(403)
        self.check(smartcar.PermissionException)

    @responses.activate
    def test_404(self):
        self.queue(404)
        self.check(smartcar.ResourceNotFoundException)

    @responses.activate
    def test_409(self):
        message = "Vehicle State Error"
        code = "VS_OO1"
        self.queue(409, message=message, code=code)
        try:
            smartcar.requester.call("GET", self.URL)
        except smartcar.StateException as err:
            self.assertEqual(err.message, message)
            self.assertEqual(err.code, code)

    @responses.activate
    def test_429(self):
        self.queue(429)
        self.check(smartcar.RateLimitingException)

    @responses.activate
    def test_430(self):
        self.queue(430)
        self.check(smartcar.MonthlyLimitExceeded)

    @responses.activate
    def test_460(self):
        self.queue(460)
        self.check(smartcar.GatewayTimeoutException)

    @responses.activate
    def test_500(self):
        self.queue(500)
        self.check(smartcar.ServerException)

    @responses.activate
    def test_smartcar_not_capable_error(self):
        self.queue(501, error="smartcar_not_capable_error", message=self.EXPECTED)
        self.check(smartcar.SmartcarNotCapableException)

    @responses.activate
    def test_vehicle_not_capable_error(self):
        self.queue(501, error="vehicle_not_capable_error", message=self.EXPECTED)
        self.check(smartcar.VehicleNotCapableException)

    @responses.activate
    def test_504(self):
        responses.add(
            "GET",
            self.URL,
            status=504,
            json={"error": "random_error", "message": self.EXPECTED},
        )
        self.check(smartcar.GatewayTimeoutException)

    @responses.activate
    def test_request_id(self):
        request_id = "1687c343-3b47-4228-ab1c-94f86850a9be"
        responses.add(
            "GET",
            self.URL,
            status=500,
            headers={"SC-Request-ID": request_id},
            json={"error": "random_error", "message": self.EXPECTED},
        )
        with self.assertRaises(smartcar.ServerException) as cm:
            smartcar.requester.call("GET", self.URL)
        self.assertEquals(cm.exception.request_id, request_id)

    @responses.activate
    def test_other(self):
        self.queue(503)
        with self.assertRaises(smartcar.SmartcarException) as cm:
            smartcar.requester.call("GET", self.URL)
        self.assertEquals(cm.exception.message, "Unexpected error")

    @responses.activate
    def test_unexpected_response(self):
        responses.add(
            "GET",
            self.URL,
            status=400,
            body="not json",
            headers={"Content-Type": "application/json"},
        )
        with self.assertRaises(smartcar.SmartcarException) as cm:
            smartcar.requester.call("GET", self.URL)
        self.assertEquals(cm.exception.message, "Unexpected error")
