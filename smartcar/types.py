from typing import TypedDict, List, NamedTuple


# ===========================================
# static.py
# ===========================================

class AllVehicles(TypedDict):
    """
    {
        "paging": {
            "count": int
            "offset": int
        } ,
        "vehicles": str[]
    }
    """

    paging: dict
    vehicles: List[str]


class GetCompatibility(TypedDict):
    """
    {
        "compatible": bool
    }
    """

    compatible: bool


# ===========================================
# vehicle.py
# ===========================================
class Meta:
    def __init__(self, **kwargs):
        for key in kwargs.keys():
            self.__dict__[key] = kwargs[key]

    def __repr__(self):
        rep = "Meta("
        keys = self.__dict__
        final = len(keys) - 1
        for i, key in enumerate(keys):
            if i == final - 1:
                rep += f"{key}={self.__dict__[key]}, "
            else:
                rep += f"{key}={self.__dict__[key]})"

        return rep


Charge = NamedTuple("Charge", [("is_plugged_in", bool), ("status", str), ("meta", Meta)])
Battery = NamedTuple("Battery", [("percent_remaining", float), ("range", float), ("meta", Meta)])
BatteryCapacity = NamedTuple("BatteryCapacity", [("capacity", float), ("meta", Meta)])
Fuel = NamedTuple("Fuel", [("range", float), ("percentRemaining", float), ("amountRemaining", float), ("meta", Meta)])
TirePressure = NamedTuple("TirePressure")
Oil = NamedTuple("Oil", [("lifeRemaining", float), ("meta", Meta)])
Odometer = NamedTuple("Odometer", [("distance", float), ("meta", Meta)])
Location = NamedTuple("Location", [("latitude", float), ("longitude", float), ("meta", Meta)])
Info = NamedTuple("Info", [("id", str), ("make", str), ("model", str), ("year", str), ("meta", Meta)])
Status = NamedTuple("Status", [("status", str), ("meta", Meta)])
Permissions = NamedTuple("Permissions", [("permissions", list), ("paging", dict), ("meta", Meta)])
