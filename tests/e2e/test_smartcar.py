import smartcar.smartcar
from smartcar import (
    get_user,
    get_vehicles,
    get_compatibility,
    hash_challenge,
    set_api_version,
    verify_payload,
    get_connections,
    delete_connections,
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


def test_get_compatibility_in_test_mode_but_no_level():
    try:
        get_compatibility(
            "WAUAFAFL1GN014882",
            scope=["read_vehicle_info"],
            options={
                "client_id": ah.CLIENT_ID,
                "client_secret": ah.CLIENT_SECRET,
                "mode": "test",
            },
        )

    except Exception as e:
        assert e.type == "VALIDATION"
        assert e.detail[0]["field"] == "test_mode_compatibility_level"
        assert (
            e.detail[0]["message"]
            == "Field must be one of: [compatible,phev,incompatible,fuel,dinosaur,bev]"
        )


def test_get_compatibility_v2():
    compatibility = smartcar.get_compatibility(
        "0SCGMCT0386A85356",
        scope=["read_odometer", "read_fuel"],
        country="US",
        options={
            "client_id": ah.CLIENT_ID,
            "client_secret": ah.CLIENT_SECRET,
            "version": "2.0",
        },
    )

    assert compatibility.compatible == True
    assert compatibility.reason == None
    assert compatibility.capabilities[0].permission == "read_odometer"
    assert compatibility.capabilities[0].endpoint == "/odometer"
    assert compatibility.capabilities[0].capable == True
    assert compatibility.capabilities[0].reason == None
    assert compatibility.capabilities[1].permission == "read_fuel"
    assert compatibility.capabilities[1].endpoint == "/fuel"
    assert compatibility.capabilities[1].capable == False
    assert compatibility.capabilities[1].reason == "VEHICLE_NOT_CAPABLE"


def test_get_compatibility_with_non_test_mode_vin():
    res = get_compatibility(
        "WAUAFAFL1GN014882",
        scope=["read_vehicle_info"],
        options={
            "client_id": ah.CLIENT_ID,
            "client_secret": ah.CLIENT_SECRET,
            "test_mode_compatibility_level": "compatible",
        },
    )
    assert res.compatible


def test_get_compatibility_without_client_id(chevy_volt):
    try:
        get_compatibility(vin=chevy_volt.vin().vin, scope=["read_vehicle_info"])
    except Exception as e:
        assert e.args == (
            '"SMARTCAR_CLIENT_ID" and "SMARTCAR_CLIENT_SECRET" environment variables must be set',
        )


def test_static_webhook_methods():
    amt = ah.APPLICATION_MANAGEMENT_TOKEN or "abc123abc123"
    hashed_challenge = hash_challenge(amt, "9c9c9c9c")
    assert verify_payload(amt, hashed_challenge, "9c9c9c9c")


def test_get_connections(bmw_for_testing_management_api):
    amt = ah.APPLICATION_MANAGEMENT_TOKEN
    connections = get_connections(
        str(amt), {"vehicle_id": bmw_for_testing_management_api}, {}
    )

    assert len(connections.connections) == 1
    assert connections.connections[0].vehicle_id == bmw_for_testing_management_api
    assert type(connections.connections[0].vehicle_id) == str
    assert type(connections.connections[0].connected_at) == str
    assert connections.paging.cursor is None


def test_delete_connections(bmw_for_testing_management_api):
    amt = ah.APPLICATION_MANAGEMENT_TOKEN
    deletions = delete_connections(
        str(amt), {"vehicle_id": bmw_for_testing_management_api}
    )
    assert len(deletions.connections) == 1
    assert deletions.connections[0].vehicle_id == bmw_for_testing_management_api
    assert type(deletions.connections[0].vehicle_id) == str
    assert deletions.connections[0].connected_at is None
