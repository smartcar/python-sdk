from typing import TypedDict, List


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
