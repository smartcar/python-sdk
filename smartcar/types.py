from collections import namedtuple
from typing import List, NamedTuple


# Return types for Smartcar API.
#
# Below are explicitly defined NamedTuples that are to be used as
# return values from Smartcar API. This will allow the SDK to provide
# type hints and dot notation, # and will help return data following
# python conventions (i.e. snake-cased attributes).
#
# 'generate_named_tuple' is used to generate an un-typed namedtuple from
# a dictionary. It will return a namedtuple that has attributes matching
# the dictionary's keys. Use this function as a catch all, or for data
# that does not have an explicit length (e.g. response headers, batch requests)
#
# Otherwise, use the explicitly defined NamedTuples for better type hints!


# ===========================================
# General
# ===========================================

def generate_named_tuple(dictionary: dict, name: str = "namedtuple") -> namedtuple:
    """
    Take a dictionary and map its keys to the attributes of a named tuple.

    Args:
        dictionary (dict): Any dictionary
        name (str): The desired name of the returned namedtuple

    Returns:
        namedtuple: With attributes matching the keys of the inputted dictionary
    """

    # Instantiate keys list, which will keep order consistent
    keys = dictionary.keys()
    if len(keys) == 0:
        return None

    attributes = ""

    for key in keys:
        formatted = key.replace("-", "_").lower()
        attributes += f" {formatted}"

    gen = namedtuple(name, attributes.strip())

    return gen._make([dictionary[k] for k in keys])


# ===========================================
# static.py
# ===========================================

Paging = NamedTuple("Paging", [("count", int), ("offset", int)])

User = NamedTuple("User", [("id", str), ("meta", namedtuple)])

Vehicles = NamedTuple(
    "Vehicles", [("vehicles", List[str]), ("paging", Paging), ("meta", namedtuple)]
)

Compatibility = NamedTuple("Compatibility", [("compatible", bool), ("meta", namedtuple)])

# ===========================================
# vehicle.py
# ===========================================

Vin = NamedTuple("Vin", [("vin", str), ("meta", namedtuple)])

Charge = NamedTuple(
    "Charge", [("is_plugged_in", bool), ("status", str), ("meta", namedtuple)]
)

Battery = NamedTuple(
    "Battery", [("percent_remaining", float), ("range", float), ("meta", namedtuple)]
)

BatteryCapacity = NamedTuple("BatteryCapacity", [("capacity", float), ("meta", namedtuple)])

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
    "tirePressure",
    [
        ("front_left", int),
        ("front_right", int),
        ("back_left", int),
        ("back_right", int),
        ("meta", namedtuple),
    ],
)

Oil = NamedTuple("Oil", [("life_remaining", float), ("meta", namedtuple)])

Odometer = NamedTuple("Odometer", [("distance", float), ("meta", namedtuple)])

Location = NamedTuple(
    "Location", [("latitude", float), ("longitude", float), ("meta", namedtuple)]
)

Info = NamedTuple(
    "Info", [("id", str), ("make", str), ("model", str), ("year", str), ("meta", namedtuple)]
)

Status = NamedTuple("Status", [("status", str), ("meta", namedtuple)])

Permissions = NamedTuple("Permissions", [("permissions", list), ("meta", namedtuple)])


# This version of Permissions will be implemented when "paging" is verified to be returned from Smartcar API:
# Permissions = NamedTuple("Permissions", [("permissions", list), ("paging", Paging), ("meta", Meta)])


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
        headers = response_or_dict["headers"]
        data = response_or_dict["body"]
    else:
        headers = response_or_dict.headers
        data = response_or_dict.json()

    # static.py
    if path == "user":
        return User(data["id"], generate_named_tuple(headers, name="Meta"))

    elif path == "vehicles":
        return Vehicles(
            data["vehicles"],
            Paging(data["paging"]["count"], data["paging"]["offset"]),
            generate_named_tuple(headers, name="Meta"),
        )

    elif path == "compatibility":
        return Compatibility(data["compatible"], generate_named_tuple(headers, name="Meta"))

    # vehicle.py
    elif path == "vin":
        return Vin(data["vin"], generate_named_tuple(headers, name="Meta"))

    elif path == "charge":
        return Charge(data["isPluggedIn"], data["state"], generate_named_tuple(headers, name="Meta"))

    elif path == "battery":
        return Battery(data["percentRemaining"], data["range"], generate_named_tuple(headers, name="Meta"))

    elif path == "battery/capacity":
        return BatteryCapacity(data["capacity"], generate_named_tuple(headers, name="Meta"))

    elif path == "fuel":
        return Fuel(
            data["range"],
            data["percentRemaining"],
            data["amountRemaining"],
            generate_named_tuple(headers, name="Meta"),
        )

    elif path == "tires/pressure":
        return TirePressure(
            data["frontLeft"],
            data["frontRight"],
            data["backLeft"],
            data["backRight"],
            generate_named_tuple(headers, name="Meta"),
        )

    elif path == "engine/oil":
        return Oil(data["lifeRemaining"], generate_named_tuple(headers, name="Meta"))

    elif path == "odometer":
        return Odometer(data["distance"], generate_named_tuple(headers, name="Meta"))

    elif path == "location":
        return Location(data["latitude"], data["longitude"], generate_named_tuple(headers, name="Meta"))

    elif path == "permissions":
        return Permissions(data["permissions"], generate_named_tuple(headers, name="Meta"))

    elif (
            path == "lock"
            or path == "unlock"
            or path == "start_charge"
            or path == "stop_charge"
            or path == "disconnect"
    ):
        return Status(data["status"], generate_named_tuple(headers, name="Meta"))

    elif path == "":
        return Info(
            data["id"],
            data["make"],
            data["model"],
            data["year"],
            generate_named_tuple(headers, name="Meta"),
        )

    elif type(data) == dict:
        return generate_named_tuple(data, "Data")

    else:
        return data
