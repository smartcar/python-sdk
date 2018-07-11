import platform
import requests
from . import exceptions as E
from . import __version__

def call(method, url, **kwargs):
    """ Attachs the kwargs into the headers, sends the request to the Smartcar API
        and handles all error cases

    Args:
        method (str): HTTP method
        url (str): url of the request
        **kwargs: parameters for the request

    Returns:
        dict: response from the request to the Smartcar API

    """
    if 'headers' not in kwargs:
        kwargs['headers'] = {}
    kwargs['headers']['User-Agent'] = 'Smartcar/{} ({}; {}) Python v{}'.format(
        __version__,
        platform.system(),
        platform.machine(),
        platform.python_version()
    )

    response = requests.request(method, url, **kwargs)
    code = response.status_code
    if response.ok:
        return response
    elif code == 400:
        raise E.ValidationException(response)
    elif code == 401:
        raise E.AuthenticationException(response)
    elif code == 403:
        raise E.PermissionException(response)
    elif code == 404:
        raise E.ResourceNotFoundException(response)
    elif code == 409:
        raise E.StateException(response)
    elif code == 429:
        raise E.RateLimitingException(response)
    elif code == 430:
        raise E.MonthlyLimitExceeded(response)
    elif code == 500:
        raise E.ServerException(response)
    elif code == 501:
        raise E.NotCapableException(response)
    elif code == 504:
        raise E.GatewayTimeoutException(response)
    else:
        response.raise_for_status()
