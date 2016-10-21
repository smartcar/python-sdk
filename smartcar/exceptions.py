class SmartcarException(Exception):
    def __init__(self, response):
        self.message = response.json()['message']

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
    pass
class RateLimitingException(SmartcarException):
    pass
class MonthlyLimitExceeded(SmartcarException):
    pass
class ServerException(SmartcarException):
    pass
class NotCapableException(SmartcarException):
    pass
class GatewayTimeoutException(SmartcarException):
    def __init__(self, response):
        self.message = response.text

    def __str__(self):
        return self.message
