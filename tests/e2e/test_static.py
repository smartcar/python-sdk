from smartcar import (
    get_user,
    get_vehicles,
    get_compatibility,
    hash_challenge,
    verify_payload,
)
from smartcar.api import Smartcar, set_api_version
from smartcar.constants import API_URL
import tests.auth_helpers as ah


def test_set_api_version(access):
    set_api_version("1.0")
    test_api = Smartcar(access.access_token)
    assert test_api.base_url == f"{API_URL}/v1.0"

    set_api_version("2.0")
    test_api2 = Smartcar(access.access_token)
    assert test_api2.base_url == f"{API_URL}/v2.0"


def test_get_user(access):
    res = get_user(access.access_token)
    assert res.id is not None


def test_get_vehicles(access):
    res = get_vehicles(access.access_token)

    assert res.vehicles is not None
    assert res.paging is not None


def test_get_compatibility(access, chevy_volt):
    res = get_compatibility(
        access.access_token,
        vin=chevy_volt.vin().vin,
        scope=["read_vehicle_info"],
        options={"client_id": ah.CLIENT_ID, "client_secret": ah.CLIENT_SECRET},
    )

    assert res.compatible is not None


def test_static_webhook_methods():
    amt = ah.APPLICATION_MANAGEMENT_TOKEN or "abc123abc123"
    hashed_challenge = hash_challenge(amt, "9c9c9c9c")
    assert verify_payload(amt, hashed_challenge, "9c9c9c9c")
