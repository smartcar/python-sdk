from smartcar import (
    get_user,
    get_vehicles,
    get_compatibility,
    hash_challenge,
    set_api_version,
    verify_payload,
)
import smartcar.config as config

import tests.auth_helpers as ah


def test_set_api_version():
    set_api_version("1.0")
    assert config.API_VERSION == "1.0"

    set_api_version("2.0")
    assert config.API_VERSION == "2.0"


def test_get_user(access):
    res = get_user(access.access_token)
    assert res.id is not None


def test_get_vehicles(access):
    res = get_vehicles(access.access_token)

    assert res.vehicles is not None
    assert res.paging is not None


def test_get_compatibility(chevy_volt):
    res = get_compatibility(
        vin=chevy_volt.vin().vin,
        scope=["read_vehicle_info"],
        options={"client_id": ah.CLIENT_ID, "client_secret": ah.CLIENT_SECRET},
    )

    assert res.compatible is not None


def test_static_webhook_methods():
    amt = ah.APPLICATION_MANAGEMENT_TOKEN or "abc123abc123"
    hashed_challenge = hash_challenge(amt, "9c9c9c9c")
    assert verify_payload(amt, hashed_challenge, "9c9c9c9c")
