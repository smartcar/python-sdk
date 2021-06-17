from typing import List, NamedTuple


# Return types for Smartcar API.
#
# Below are explicitly defined NamedTuples that are to be used as
# return values from Smartcar API. This will allow the SDK to provide
# type hints and dot notation, # and will help return data following
# python conventions (i.e. snake-cased attributes).
#
# However, classes 'Meta' and 'Batch' are used to generate objects from
# dictionaries with variable amounts of keys. This allows for flexibility.
# Although it's possible to use these classes as general return types,
# please try to use one of the pre-defined NamedTuples or create/define a new one.
# This will allow for better type hints and performance. NamedTuples
# use __slots__ for attributes instead of a dictionary.

# ===========================================
# General
# ===========================================


class Meta:
    """
    Class for transforming a dictionary (with a variable number
    of keys) into an object with attributes. Attribute names represent
    a lower-cased response header that had its hyphens replaced with
    underscores. Each attribute represents the actual,
    unadulterated response header.
    """

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            formatted = key.replace("-", "_").lower()
            self.__dict__[formatted] = kwargs[key]

    def __repr__(self):
        rep = "\n\nResponse Headers: {"
        last_idx = len(self.__dict__.keys()) - 1

        for i, key in enumerate(self.__dict__.keys()):
            if i < last_idx:
                rep += f"\n\t{key}: {self.__dict__[key]},"
            else:
                rep += f"\n\t{key}: {self.__dict__[key]}"

        rep += "\n}\n"
        return rep


class Batch:
    """
    Class for transforming a dictionary (with a variable number
    of keys) into an object with attributes. Attribute names represent
    the paths that the user requested in a Smartcar Batch requests.
    Attributes contain the appropriate NamedTuple for the request.

    e.g. <vehicle>.batch(['/odometer', '/location']) ->
    Batch <Odometer> <Location>

    Response headers (i.e. a Meta object) can be attached to Batch
    afterward.
    """

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            self.__dict__[key] = kwargs[key]

    def __repr__(self):
        rep = "\nBatch: "
        last_idx = len(self.__dict__.keys()) - 1

        for i, key in enumerate(self.__dict__.keys()):
            if i < last_idx:
                rep += f"<{key}>, "
            else:
                rep += f"<{key}>"

        return rep


Paging = NamedTuple("Paging", [("count", int), ("offset", int)])

# ===========================================
# static.py
# ===========================================

User = NamedTuple("User", [("id", str), ("meta", Meta)])

Vehicles = NamedTuple(
    "Vehicles", [("vehicles", List[str]), ("paging", Paging), ("meta", Meta)]
)

Compatibility = NamedTuple("Compatibility", [("compatible", bool), ("meta", Meta)])

# ===========================================
# vehicle.py
# ===========================================

Vin = NamedTuple("Vin", [("vin", str), ("meta", Meta)])

Charge = NamedTuple(
    "Charge", [("is_plugged_in", bool), ("status", str), ("meta", Meta)]
)

Battery = NamedTuple(
    "Battery", [("percent_remaining", float), ("range", float), ("meta", Meta)]
)

BatteryCapacity = NamedTuple("BatteryCapacity", [("capacity", float), ("meta", Meta)])

Fuel = NamedTuple(
    "Fuel",
    [
        ("range", float),
        ("percent_remaining", float),
        ("amount_remaining", float),
        ("meta", Meta),
    ],
)

TirePressure = NamedTuple(
    "tirePressure",
    [
        ("front_left", int),
        ("front_right", int),
        ("back_left", int),
        ("back_right", int),
        ("meta", Meta),
    ],
)

Oil = NamedTuple("Oil", [("life_remaining", float), ("meta", Meta)])

Odometer = NamedTuple("Odometer", [("distance", float), ("meta", Meta)])

Location = NamedTuple(
    "Location", [("latitude", float), ("longitude", float), ("meta", Meta)]
)

Info = NamedTuple(
    "Info", [("id", str), ("make", str), ("model", str), ("year", str), ("meta", Meta)]
)

Status = NamedTuple("Status", [("status", str), ("meta", Meta)])

Permissions = NamedTuple("Permissions", [("permissions", list), ("meta", Meta)])


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
        return User(data["id"], Meta(**headers))

    elif path == "vehicles":
        return Vehicles(
            data["vehicles"],
            Paging(data["paging"]["count"], data["paging"]["offset"]),
            Meta(**headers),
        )

    elif path == "compatibility":
        return Compatibility(data["compatible"], Meta(**headers))

    # vehicle.py
    elif path == "vin":
        return Vin(data["vin"], Meta(**headers))

    elif path == "charge":
        return Charge(data["isPluggedIn"], data["state"], Meta(**headers))

    elif path == "battery":
        return Battery(data["percentRemaining"], data["range"], Meta(**headers))

    elif path == "battery/capacity":
        return BatteryCapacity(data["capacity"], Meta(**headers))

    elif path == "fuel":
        return Fuel(
            data["range"],
            data["percentRemaining"],
            data["amountRemaining"],
            Meta(**headers),
        )

    elif path == "tires/pressure":
        return TirePressure(
            data["frontLeft"],
            data["frontRight"],
            data["backLeft"],
            data["backRight"],
            Meta(**headers),
        )

    elif path == "engine/oil":
        return Oil(data["lifeRemaining"], Meta(**headers))

    elif path == "odometer":
        return Odometer(data["distance"], Meta(**headers))

    elif path == "location":
        return Location(data["latitude"], data["longitude"], Meta(**headers))

    elif path == "permissions":
        return Permissions(data["permissions"], Meta(**headers))

    elif (
        path == "lock"
        or path == "unlock"
        or path == "start_charge"
        or path == "stop_charge"
        or path == "disconnect"
    ):
        return Status(data["status"], Meta(**headers))

    elif path == "":
        return Info(
            data["id"],
            data["make"],
            data["model"],
            data["year"],
            Meta(**headers),
        )

    else:
        return data
