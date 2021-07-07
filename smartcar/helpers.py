import os
import platform
import requests

import smartcar.exception as sce
from smartcar import __version__


def requester(method: str, url: str, **kwargs) -> requests.models.Response:
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
            raise sce.exception_factory(code, headers, body)

    except Exception as e:
        if isinstance(e, sce.SmartcarException):
            raise e
        else:
            raise sce.SmartcarException(message="SDK_ERROR") from e


def validate_env(test_mode: bool = False) -> None:
    """
    Helper Function to determine if environment variables for client id
    and secret are set properly.

    Args:
        test_mode: bool

    Raises:
        Basic Exception
    """
    prefix = "E2E_SMARTCAR" if test_mode else "SMARTCAR"

    if (
        f"{prefix}_CLIENT_ID" not in os.environ
        or f"{prefix}_CLIENT_SECRET" not in os.environ
    ):
        raise Exception(
            f'"{prefix}_CLIENT_ID", "{prefix}_CLIENT_SECRET", and '
            f'"{prefix}_CLIENT_REDIRECT_URI environment variables must be set'
        )


def format_flag_query(flags: dict) -> str:
    """
    Takes a dictionary of flags and parses it into a space separated
    string:  "<key>:<value> <key>:<value> ..." to be injected
    as a query parameter.

    Args:
        flags: dict

    Returns:
        str, space separated with "<key>:<value"

        e.g.
        flags == {"flag1 : True, "color" : "green"}
        -> "flag1:True color:green:
    """
    flags_str = ""

    for flag in flags.keys():
        flags_str += f"{flag}:{flags[flag]} "

    return flags_str.strip()


def format_path_and_attribute_for_batch(raw_path: str) -> tuple:
    """
    Prettify the batch attribute and path names.
    Returned formatted_path will have the slash sliced off.
    Returned formatted_attribute will be attached to the final return of vehicle.batch().
    The naming of the attribute should consider empty and nested paths.

    Args:
        raw_path: Raw path (minus the slash) to smartcar endpoint

    Returns:
        (<formatted path>, <formatted attribute>)

        e.g.
        1. "EMPTY" raw_path  == '/' -> ('', 'attributes')
        2. "NORMAL" raw_path == '/odometer' -> ('odometer', 'odometer')
        3. "NESTED" raw_path == '/engine/oil' -> ('engine/oil', 'engine_oil')
    """
    mapper = {
        "battery/capacity": "battery_capacity",
        "engine/oil": "engine_oil",
        "tires/pressure": "tire_pressure",
        "": "attributes",
    }
    formatted_path = raw_path[1:] if raw_path[0] == "/" else raw_path
    formatted_attribute = mapper.get(formatted_path, formatted_path)
    return formatted_path, formatted_attribute
