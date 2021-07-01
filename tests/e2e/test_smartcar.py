import smartcar.smartcar
from smartcar import (
    get_user,
    get_vehicles,
    get_compatibility,
    hash_challenge,
    set_api_version,
    verify_payload,
)
import smartcar.types as types
import tests.auth_helpers as ah


def test_set_and_get_api_version():
    set_api_version("1.0")
    assert smartcar.smartcar.API_VERSION == "1.0"
    assert smartcar.smartcar.get_api_version() == "1.0"

    set_api_version("2.0")
    assert smartcar.smartcar.API_VERSION == "2.0"
    assert smartcar.smartcar.get_api_version() == "2.0"


def test_get_user_and_meta_request_id(access):
    res = get_user(access.access_token)
    assert res.id is not None
    assert res.meta.request_id is not None


def test_get_vehicles(access):
    res = get_vehicles(access.access_token)
    assert res.vehicles is not None
    assert res.paging is not None
    assert type(res.paging) == types.Paging


def test_get_vehicles_with_paging(access):
    paging = {"limit": 1, "offset": 1}
    res = get_vehicles(access.access_token, paging)
    assert res.paging.offset == 1
    assert len(res.vehicles) == 0


def test_get_compatibility_with_flags(chevy_volt):
    res = get_compatibility(
        vin=chevy_volt.vin().vin,
        scope=["read_vehicle_info"],
        options={
            "client_id": ah.CLIENT_ID,
            "client_secret": ah.CLIENT_SECRET,
            "flags": {"flag1": True},
        },
    )

    assert res.compatible is not None


def test_get_compatibility_without_client_id(chevy_volt):
    try:
        get_compatibility(vin=chevy_volt.vin().vin, scope=["read_vehicle_info"])
    except Exception as e:
        assert e.args == (
            '"SMARTCAR_CLIENT_ID", "SMARTCAR_CLIENT_SECRET", and "SMARTCAR_CLIENT_REDIRECT_URI environment variables must be set',
        )


def test_static_webhook_methods():
    amt = ah.APPLICATION_MANAGEMENT_TOKEN or "abc123abc123"
    hashed_challenge = hash_challenge(amt, "9c9c9c9c")
    assert verify_payload(amt, hashed_challenge, "9c9c9c9c")
