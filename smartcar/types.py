import datetime
from collections import namedtuple
from typing import List, NamedTuple
import re
import requests.structures as rs


# Return types for Smartcar API.
#
# 'generate_named_tuple' is used to generate an un-typed namedtuple from
# a dictionary. It will return a namedtuple that has attributes matching
# the dictionary's keys. Use this function as a catch all, or for data
# that does not have an explicit length (e.g. response headers, batch requests)
#
# Otherwise, use the explicitly defined NamedTuples for better type hints!


def generate_named_tuple(
    dictionary: dict, name: str = "namedtuple", kebab_case=False
) -> namedtuple:
    """
    Take a dictionary and map its keys to the attributes of a named tuple.

    Args:
        dictionary (dict): Any dictionary
        name (str): The desired name of the returned namedtuple
        kebab_case (bool): format kebab-cased keys, otherwise handle camelCased keys

    Returns:
        namedtuple: With attributes matching the keys of the inputted dictionary
    """

    # Instantiate keys list, which will keep order consistent
    keys = dictionary.keys()
    if len(keys) == 0:
        return None

    attributes = []

    for key in keys:
        # Convert kebab to snake case, if relevant
        if kebab_case:
            formatted = key.replace("-", "_").lower()

        # convert camel to snake case (using regex function)
        else:
            formatted = _camel_to_snake(key)

        attributes.append(formatted)

    gen = namedtuple(name, attributes)

    return gen._make([dictionary[k] for k in keys])


def _camel_to_snake(camel_string: str) -> str:
    """
    Use regex to change camelCased string to snake_case

    Args:
        camel_string(str)

    Returns:
        A snake_cased string

    """
    result = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", camel_string)
    result = re.sub("(.)([0-9]+)", r"\1_\2", result)
    result = re.sub("([a-z0-9])([A-Z])", r"\1_\2", result)
    return result.lower()


def build_meta(response_headers: rs.CaseInsensitiveDict) -> namedtuple:
    smartcar_headers = {
        "sc-data-age": "data_age",
        "sc-unit-system": "unit_system",
        "sc-request-id": "request_id",
    }

    meta_dict = {}
    for key, value in smartcar_headers.items():
        if key in response_headers:
            meta_dict[value] = response_headers[key]

    return generate_named_tuple(meta_dict, "Meta", True)


# ===========================================
# auth_client.py
# ===========================================

Access = NamedTuple(
    "Access",
    [
        ("access_token", str),
        ("token_type", str),
        ("expires_in", int),
        ("expiration", datetime.datetime),
        ("refresh_token", str),
        ("refresh_expiration", datetime.datetime),
    ],
)


def make_access_object(access: dict) -> Access:
    return Access(
        access.get("access_token"),
        access.get("token_type"),
        access.get("expires_in"),
        access.get("expiration"),
        access.get("refresh_token"),
        access.get("refresh_expiration"),
    )


# ===========================================
# smartcar.py
# ===========================================

Paging = NamedTuple("Paging", [("count", int), ("offset", int)])

User = NamedTuple("User", [("id", str), ("meta", namedtuple)])

Vehicles = NamedTuple(
    "Vehicles",
    [("vehicles", List[str]), ("paging", Paging), ("meta", namedtuple)],
)

Compatibility = NamedTuple(
    "Compatibility", [("compatible", bool), ("meta", namedtuple)]
)

# ===========================================
# vehicle.py
# ===========================================

Vin = NamedTuple("Vin", [("vin", str), ("meta", namedtuple)])

Charge = NamedTuple(
    "Charge",
    [("is_plugged_in", bool), ("state", str), ("meta", namedtuple)],
)

Battery = NamedTuple(
    "Battery",
    [("percent_remaining", float), ("range", float), ("meta", namedtuple)],
)

BatteryCapacity = NamedTuple(
    "BatteryCapacity", [("capacity", float), ("meta", namedtuple)]
)

Fuel = NamedTuple(
    "Fuel",
    [
        ("range", float),
        ("percent_remaining", float),
        ("amount_remaining", float),
        ("meta", namedtuple),
    ],
)

TirePressure = NamedTuple(
    "TirePressure",
    [
        ("front_left", int),
        ("front_right", int),
        ("back_left", int),
        ("back_right", int),
        ("meta", namedtuple),
    ],
)

EngineOil = NamedTuple("EngineOil", [("life_remaining", float), ("meta", namedtuple)])

Odometer = NamedTuple("Odometer", [("distance", float), ("meta", namedtuple)])

Location = NamedTuple(
    "Location",
    [("latitude", float), ("longitude", float), ("meta", namedtuple)],
)

Attributes = NamedTuple(
    "Attributes",
    [
        ("id", str),
        ("make", str),
        ("model", str),
        ("year", str),
        ("meta", namedtuple),
    ],
)

Action = NamedTuple("Action", [("status", str), ("message", str), ("meta", namedtuple)])

Status = NamedTuple("Status", [("status", str), ("meta", namedtuple)])

Permissions = NamedTuple(
    "Permissions", [("permissions", list), ("paging", Paging), ("meta", namedtuple)]
)

Subscribe = NamedTuple(
    "Subscribe",
    [("webhook_id", str), ("vehicle_id", str), ("meta", namedtuple)],
)

# ===========================================
# Named Tuple Selector Function
# ===========================================


def select_named_tuple(path: str, response_or_dict) -> NamedTuple:
    """
    This function is used to select one of the pre-defined NamedTuples
    based on a path provided. Upon selection, the appropriate NamedTuple
    will be instantiated and returned. This function can take in a
    response from Smartcar API OR a dictionary with "body", "headers",
    "path", and "status".

    The only use case for the parsing of a dictionary (rather than a response)
    would be for "batch" calls to Smartcar API. Upon sending a batch request
    to SmartcarAPI, a single response is returned. The response data
    (i.e. response.json()) contains a list of dictionaries, each dictionary
    representing the result of each request in the batch. For this reason,
    this function needs to be able to parse a dictionary as well.

    Note that if a path is not dictated in one of the
    conditionals below, the raw data will be returned. This, in theory,
    shouldn't run because paths are defined by the contributing developer.
    In the case of "batch" requests, incorrect paths to batch will result in
    a SmartcarException before this function is called.

    Args:
        path (str): Smartcar API path
        response_or_dict: Smartcar response, or a dictionary after parsing
            the response to the "batch" endpoint

    Returns:
        NamedTuple: Appropriate to the path.

    """
    if type(response_or_dict) == dict:
        headers_dict = rs.CaseInsensitiveDict(response_or_dict["headers"])
        headers = build_meta(headers_dict)
        data = response_or_dict["body"]
    else:
        headers = build_meta(response_or_dict.headers)
        data = response_or_dict.json()

    # smartcar.py
    if path == "user":
        return User(data["id"], headers)

    elif path == "vehicles":
        return Vehicles(
            data["vehicles"],
            Paging(data["paging"]["count"], data["paging"]["offset"]),
            headers,
        )

    elif path == "compatibility":
        return Compatibility(data["compatible"], headers)

    # vehicle.py
    elif path == "vin":
        return Vin(data["vin"], headers)

    elif path == "charge":
        return Charge(data["isPluggedIn"], data["state"], headers)

    elif path == "battery":
        return Battery(data["percentRemaining"], data["range"], headers)

    elif path == "battery/capacity":
        return BatteryCapacity(data["capacity"], headers)

    elif path == "fuel":
        return Fuel(
            data["range"],
            data["percentRemaining"],
            data["amountRemaining"],
            headers,
        )

    elif path == "tires/pressure":
        return TirePressure(
            data["frontLeft"],
            data["frontRight"],
            data["backLeft"],
            data["backRight"],
            headers,
        )

    elif path == "engine/oil":
        return EngineOil(data["lifeRemaining"], headers)

    elif path == "odometer":
        return Odometer(data["distance"], headers)

    elif path == "location":
        return Location(data["latitude"], data["longitude"], headers)

    elif path == "permissions":
        return Permissions(
            data["permissions"],
            Paging(data["paging"]["count"], data["paging"]["offset"]),
            headers,
        )

    elif path == "subscribe":
        return Subscribe(data["webhookId"], data["vehicleId"], headers)

    elif (
        path == "lock"
        or path == "unlock"
        or path == "start_charge"
        or path == "stop_charge"
    ):
        return Action(data["status"], data["message"], headers)

    elif path == "disconnect" or path == "unsubscribe":
        return Status(data["status"], headers)

    elif path == "":
        return Attributes(
            data["id"],
            data["make"],
            data["model"],
            data["year"],
            headers,
        )

    elif type(data) == dict:
        return generate_named_tuple(data, "Data")

    else:
        return data
