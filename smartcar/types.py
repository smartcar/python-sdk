from typing import List, NamedTuple


# ===========================================
# General
# ===========================================

class Meta:
    def __init__(self, **kwargs):
        for key in kwargs.keys():
            self.__dict__[key] = kwargs[key]

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


Paging = NamedTuple("Paging", [("count", int), ("offset", int)])

# ===========================================
# static.py
# ===========================================

User = NamedTuple("User", [("id", str), ("meta", Meta)])

Vehicles = NamedTuple("Vehicles", [("vehicles", List[str]), ("paging", Paging), ("meta", Meta)])

Compatibility = NamedTuple("Compatibility", [("compatible", bool), ("meta", Meta)])

# ===========================================
# vehicle.py
# ===========================================


Charge = NamedTuple("Charge", [("is_plugged_in", bool), ("status", str), ("meta", Meta)])

Battery = NamedTuple("Battery", [("percent_remaining", float), ("range", float), ("meta", Meta)])

BatteryCapacity = NamedTuple("BatteryCapacity", [("capacity", float), ("meta", Meta)])

Fuel = NamedTuple("Fuel", [("range", float), ("percent_remaining", float), ("amount_remaining", float), ("meta", Meta)])

TirePressure = NamedTuple("tirePressure",
                          [("front_left", int), ("front_right", int), ("back_left", int), ("back_right", int),
                           ("meta", Meta)])

Oil = NamedTuple("Oil", [("life_remaining", float), ("meta", Meta)])

Odometer = NamedTuple("Odometer", [("distance", float), ("meta", Meta)])

Location = NamedTuple("Location", [("latitude", float), ("longitude", float), ("meta", Meta)])

Info = NamedTuple("Info", [("id", str), ("make", str), ("model", str), ("year", str), ("meta", Meta)])

Status = NamedTuple("Status", [("status", str), ("meta", Meta)])

Permissions = NamedTuple("Permissions", [("permissions", list), ("paging", dict), ("meta", Meta)])
