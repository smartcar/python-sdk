import unittest
import responses
import requests
import smartcar

class TestRequester(unittest.TestCase):
    EXPECTED = 'expected'
    URL = 'http://fake.url'

    def queue(self, code, **kwargs):
        """ queue up a fake response with the specified status code """
        if not kwargs:
            json = { 'message': self.EXPECTED }
        else:
            json = kwargs

        responses.add('GET', self.URL, status=code, json=json)

    def check(self, exception):

        self.assertRaisesRegexp(exception, self.EXPECTED,
            smartcar.requester.call, 'GET', self.URL)

    @responses.activate
    def test_user_agent(self):
        self.queue(200)
        smartcar.requester.call('GET', self.URL)
        agent = 'smartcar-python-sdk:{}'.format(smartcar.__version__)
        self.assertEqual(responses.calls[0].request.headers['User-Agent'], agent)

    @responses.activate
    def test_oauth_error(self):
        self.queue(401, error_description='unauthorized')
        try:
            smartcar.requester.call('GET', self.URL)
        except smartcar.AuthenticationException as err:
            self.assertEqual(err.message, 'unauthorized')

    @responses.activate
    def test_unknown_error(self):
        self.queue(401, unknown_field='unknown error')
        try:
            smartcar.requester.call('GET', self.URL)
        except smartcar.AuthenticationException as err:
            self.assertEqual(err.message, 'Unknown error')

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
        self.queue(409)
        self.check(smartcar.StateException)

    @responses.activate
    def test_429(self):
        self.queue(429)
        self.check(smartcar.RateLimitingException)

    @responses.activate
    def test_430(self):
        self.queue(430)
        self.check(smartcar.MonthlyLimitExceeded)

    @responses.activate
    def test_500(self):
        self.queue(500)
        self.check(smartcar.ServerException)

    @responses.activate
    def test_501(self):
        self.queue(501)
        self.check(smartcar.NotCapableException)

    @responses.activate
    def test_504(self):
        responses.add('GET', self.URL, status=504, body=self.EXPECTED)
        self.check(smartcar.GatewayTimeoutException)

    @responses.activate
    def test_other(self):
        self.queue(503)
        with self.assertRaises(requests.exceptions.HTTPError):
            smartcar.requester.call('GET', self.URL)
