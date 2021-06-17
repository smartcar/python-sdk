from smartcar import get_user, get_vehicles, get_compatibility, set_api_version
from smartcar.api import Smartcar
from smartcar.constants import API_URL
import tests.auth_helpers as ah


def test_set_api_version(access_object):
    access_token = access_object.get("access_token")

    set_api_version("1.0")
    test_api = Smartcar(access_token)
    assert test_api.base_url == f"{API_URL}/v1.0"

    set_api_version("2.0")
    test_api2 = Smartcar(access_token)
    assert test_api2.base_url == f"{API_URL}/v2.0"


def test_get_user(access_object):
    access_token = access_object.get("access_token")
    res = get_user(access_token)

    assert res.id is not None


def test_get_vehicles(access_object):
    access_token = access_object.get("access_token")
    res = get_vehicles(access_token)

    assert res.vehicles is not None
    assert res.paging is not None


def test_get_compatibility(access_object, chevy_volt):
    access_token = access_object.get("access_token")
    res = get_compatibility(
        access_token,
        vin=chevy_volt.vin().vin,
        scope=["read_vehicle_info"],
        options={"client_id": ah.CLIENT_ID, "client_secret": ah.CLIENT_SECRET},
    )

    assert res.compatible is not None
