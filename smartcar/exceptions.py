import requests


class SmartcarException(Exception):
    def __init__(self, response):
        self.message = "Unknown error"
        if type(response) is requests.models.Response:
            json = response.json()
            self.request_id = response.headers.get("sc-request-id")
            if "message" in json:
                self.message = json["message"]
            elif "error_description" in json:
                self.message = json["error_description"]
        elif type(response) is str:
            self.message = response

    def __str__(self):
        return self.message


class SmartcarExceptionV2(Exception):
    """ Exceptions throw by v2.0 endpoints """

    def __init__(self, response):
        if type(response) is requests.models.Response:
            json = response.json()
            if "type" in json:
                self.type = json["type"]
                self.code = json["code"]
                self.description = json["description"]
                self.doc_url = json["docURL"]
                self.status_code = json["statusCode"]
                self.request_id = json["requestId"]
                self.resolution = json["resolution"]
                self.detail = json["detail"]
            elif "error_description" in json:
                self.error_description = json["error_description"]
                self.error = json["error"]
                self.error_uri = json["error_uri"]
        elif type(response) is str:
            self.description = response

    def __str__(self):
        return self.description


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
        self.code = json["code"]

    def __str__(self):
        return self.code + ": " + self.message


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
