import platform
import requests

import smartcar.exception as sce
from smartcar import __version__


def call(method: str, url: str, **kwargs) -> requests.models.Response:
    """
    Attaches the kwargs into the headers, sends the request to the Smartcar API
        and handles all error cases

    Args:
        method (str): HTTP method
        url (str): url of the request
        **kwargs: parameters for the request

    Returns:
        requests.models.Response: response from the request to the Smartcar API
    """
    if "headers" not in kwargs:
        kwargs["headers"] = {}

    kwargs["headers"]["User-Agent"] = (
        f"Smartcar/{__version__}({platform.system()}; "
        f"{platform.machine()}) Python v{platform.python_version()}"
    )

    try:
        response = requests.request(method, url, timeout=310, **kwargs)
        code = response.status_code
        headers = response.headers
        body = response.text

        if response.ok:
            return response
        else:
            sce.exception_factory(code, headers, body)

    except Exception as e:
        import ipdb
        ipdb.set_trace()
        if isinstance(e, sce.SmartcarException):
            raise e
        else:
            raise sce.SmartcarException(message="SDK_ERROR") from e
