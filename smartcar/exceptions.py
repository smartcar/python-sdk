class SmartcarException(Exception):
    def __init__(self, response):
        json = response.json()
        if 'message' in json:
            self.message = json['message']
        elif 'error_description' in json:
            self.message = json['error_description']
        else:
            self.message = 'Unknown error'

    def __str__(self):
        return self.message


class ValidationException(SmartcarException):
    pass


class AuthenticationException(SmartcarException):
    pass


class PermissionException(SmartcarException):
    pass


class ResourceNotFoundException(SmartcarException):
    pass


class StateException(SmartcarException):
    def __init__(self, response):
        super(StateException, self).__init__(response)
        json = response.json()
        self.code = json['code']

    def __str__(self):
        return self.code + ': ' + self.message


class RateLimitingException(SmartcarException):
    pass


class MonthlyLimitExceeded(SmartcarException):
    pass


class ServerException(SmartcarException):
    pass


class VehicleNotCapableException(SmartcarException):
    pass


class SmartcarNotCapableException(SmartcarException):
    pass


class GatewayTimeoutException(SmartcarException):
    def __init__(self, response):
        self.message = response.text

    def __str__(self):
        return self.message
