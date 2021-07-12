import json


class SmartcarException(Exception):
    """
    All exceptions with this SDK will be a Smartcar Exception. v1.0 errors and
    v2.0 errors are distinguished by the response body. "General" exceptions will
    be raised as "SDK ERRORS".
    """

    def __init__(self, **kwargs):
        # populate the error with passed in keys.
        for key in kwargs.keys():
            # format resolution: must be a dictionary with "type" and "url"
            if key == "resolution":
                if type((kwargs[key])) == str:
                    formatted_resolution = {"type": kwargs[key], "url": None}
                    self.__dict__[key] = formatted_resolution
                if type(kwargs[key]) == dict:
                    formatted_resolution = {
                        "type": kwargs[key].get("type"),
                        "url": kwargs[key].get("url"),
                    }
                    self.__dict__[key] = formatted_resolution
                else:
                    self.__dict__[key] = {"type": None, "url": None}
            else:
                self.__dict__[key] = kwargs[key] or None

        # v2.0
        if "type" in kwargs and "code" in kwargs and "description" in kwargs:
            code = f":{kwargs.get('code')}" if kwargs.get("code") else ""
            self.message = f"{kwargs['type']}{code} - {kwargs['description']}"

        # v1.0
        else:
            self.message = kwargs.get("message")

        super().__init__(self.message)


def exception_factory(status_code: int, headers: dict, body: str):
    # v1.0 Exception: Content type other than application/json
    if "application/json" not in headers["Content-Type"]:
        return SmartcarException(status_code=status_code, message=body)

    # Parse body into JSON. Throw SDK error if this fails.
    try:
        response = json.loads(body)
    except Exception:
        return SmartcarException(
            status_code=status_code,
            request_id=headers.get("SC-Request-Id"),
            type="SDK_ERROR",
            message=body,
        )

    # v1.0 with code or OAuth error
    if response.get("error"):
        if response.get("message"):
            # smartcar v1
            return SmartcarException(
                status_code=response.get("statusCode"),
                request_id=response.get("requestId"),
                type=response.get("error"),
                message=response.get("message"),
                code=response.get("code"),
            )
        elif response.get("error_description"):
            # OAuth error
            return SmartcarException(
                status_code=status_code,
                type=response.get("error"),
                message=response.get("error_description"),
            )

    # v2.0
    elif response.get("type"):
        return SmartcarException(
            status_code=response.get("statusCode"),
            request_id=response.get("requestId"),
            type=response.get("type"),
            description=response.get("description"),
            code=response.get("code"),
            doc_url=response.get("docURL"),
            resolution=response.get("resolution"),
            detail=response.get("detail"),
        )

    # Weird...
    else:
        return SmartcarException(
            status_code=status_code,
            request_id=headers["SC-Request-Id"],
            type="SDK_ERROR",
            message=body,
        )
