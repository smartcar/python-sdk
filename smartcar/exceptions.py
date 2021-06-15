import requests


class SmartcarException(Exception):
    def __init__(self, response):
        self.message = "Unknown error"
        if type(response) is requests.models.Response:
            content_type = response.headers["Content-Type"]
            if "application/json" in content_type:
                json = response.json()
                self.request_id = response.headers.get("sc-request-id")
                if "message" in json:
                    self.message = json["message"]
                elif "error_description" in json:
                    self.message = json["error_description"]
            elif "text/html" in content_type:
                self.message = response.text
        elif type(response) is str:
            self.message = response

    def __str__(self):
        return self.message


class SmartcarExceptionV2(SmartcarException):
    """
    Exceptions throw by v2.0 endpoints
    """

    def __init__(self, response):
        self.type = None
        if type(response) is requests.models.Response:
            content_type = response.headers["Content-Type"]
            if "application/json" in content_type:
                json = response.json()
                self.type = json["type"]
                self.code = json["code"]
                self.description = json["description"]
                self.doc_url = json["docURL"]
                self.status_code = json["statusCode"]
                self.request_id = json["requestId"]
                self.resolution = json["resolution"]
                if "detail" in json:
                    self.detail = json["detail"]
            elif "text/html" in content_type:
                self.description = response.text
        elif type(response) is str:
            self.description = response

    def __str__(self):
        if self.type is not None:
            return "{}:{} - {}".format(self.type, self.code, self.description)
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
