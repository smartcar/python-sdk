import smartcar.types as types
from smartcar.exception import SmartcarException
import tests.auth_helpers as ah


# Tests
def test_vin_and_meta(chevy_volt):
    vin = chevy_volt.vin()
    assert vin is not None
    assert type(vin) == types.Vin
    assert vin._fields == ("vin", "meta")
    assert isinstance(vin.meta, tuple)


def test_charge(chevy_volt):
    charge = chevy_volt.charge()
    assert charge is not None
    assert type(charge) == types.Charge
    assert charge._fields == ("is_plugged_in", "state", "meta")
    assert charge.is_plugged_in is not None


def test_battery(chevy_volt):
    battery = chevy_volt.battery()
    assert battery is not None
    assert type(battery) == types.Battery
    assert battery._fields == ("percent_remaining", "range", "meta")


def test_battery_capacity(chevy_volt):
    battery_capacity = chevy_volt.battery_capacity()
    assert battery_capacity is not None
    assert type(battery_capacity) == types.BatteryCapacity
    assert battery_capacity._fields == ("capacity", "meta")


def test_fuel(chevy_volt):
    fuel = chevy_volt.fuel()
    assert fuel is not None
    assert type(fuel) == types.Fuel
    assert fuel._fields == ("range", "percent_remaining", "amount_remaining", "meta")


def test_tire_pressure(chevy_volt):
    tire_pressure = chevy_volt.tire_pressure()
    assert tire_pressure is not None
    assert type(tire_pressure) == types.TirePressure
    assert tire_pressure._fields == (
        "front_left",
        "front_right",
        "back_left",
        "back_right",
        "meta",
    )


def test_engine_oil(chevy_volt):
    engine_oil = chevy_volt.engine_oil()
    assert engine_oil is not None
    assert type(engine_oil) == types.EngineOil
    assert engine_oil._fields == ("life_remaining", "meta")


def test_odometer(chevy_volt):
    odometer = chevy_volt.odometer()
    assert odometer is not None
    assert type(odometer) == types.Odometer
    assert odometer._fields == ("distance", "meta")


def test_location(chevy_volt):
    location = chevy_volt.location()
    assert location is not None
    assert type(location) == types.Location
    assert location._fields == ("latitude", "longitude", "meta")


def test_attributes(chevy_volt):
    attributes = chevy_volt.attributes()
    assert attributes is not None
    assert type(attributes) == types.Attributes
    assert attributes._fields == ("id", "make", "model", "year", "meta")

def test_get_charge_limit(chevy_volt):
    charge_limit = chevy_volt.get_charge_limit()
    assert charge_limit is not None
    assert type(charge_limit) == types.ChargeLimit
    assert charge_limit._fields == ("limit", "meta")

def test_lock(chevy_volt):
    response = chevy_volt.lock()
    assert response.status == "success"
    assert type(response) == types.Action
    assert response._fields == ("status", "message", "meta")


def test_unlock(chevy_volt):
    response = chevy_volt.unlock()
    assert response.status == "success"
    assert type(response) == types.Action
    assert response._fields == ("status", "message", "meta")


def test_start_charge(ford_car):
    response = ford_car.start_charge()
    assert response.status == "success"
    assert type(response) == types.Action
    assert response._fields == ("status", "message", "meta")


def test_stop_charge(ford_car):
    response = ford_car.stop_charge()
    assert response.status == "success"
    assert type(response) == types.Action
    assert response._fields == ("status", "message", "meta")

def test_set_charge_limit(chevy_volt):
    response = chevy_volt.set_charge_limit(0.7)
    assert response.status == "success"
    assert type(response) == types.Action
    assert response._fields == ("status", "message", "meta")

def test_batch_success(chevy_volt):
    batch = chevy_volt.batch(["/odometer", "/location"])
    assert batch is not None
    assert batch._fields == ("odometer", "location", "meta")
    assert isinstance(batch.meta, tuple)
    assert isinstance(batch.odometer().meta, tuple)
    assert batch.odometer().distance is not None
    assert batch.odometer().meta.request_id is not None
    assert batch.location().longitude is not None
    assert batch.location().latitude is not None
    assert batch.location().meta.request_id is not None


def test_batch_misspelled_permission(chevy_volt):
    try:
        chevy_volt.batch(["/odometer", "/LOCATIONNNNNNNN"])
    except Exception as e:
        assert e.status_code == 400
        assert e.type == "VALIDATION"


def test_batch_unauthorized_permission(chevy_volt_limited_scope):
    """
    Test for weird path names (empty or nested, e.g. '' or 'engine/oil')
    Test for error attachment on out of scope permissions

    In scope: "/", "/odometer", "/engine/oil"
    Out of scope: "/location
    """
    batch = chevy_volt_limited_scope.batch(
        ["/", "/odometer", "/engine/oil", "/location"]
    )
    assert batch.attributes().make is not None
    assert batch.odometer().distance is not None
    assert batch.engine_oil().life_remaining is not None
    try:
        batch.location()
    except Exception as e:
        assert isinstance(e, SmartcarException)
        assert e.status_code == 403


def test_batch_unauthorized_permission_v1(chevy_volt_limited_scope):
    chevy_volt_limited_scope._api_version = "1.0"
    batch = chevy_volt_limited_scope.batch(["/odometer", "/location"])
    try:
        batch.location()
    except Exception as e:
        assert isinstance(e, SmartcarException)
        assert e.status_code == 403
    finally:
        chevy_volt_limited_scope._api_version = "2.0"


def test_permissions(chevy_volt):
    permissions = chevy_volt.permissions()
    assert permissions is not None
    assert type(permissions) == types.Permissions
    assert permissions._fields == ("permissions", "paging", "meta")


def test_permissions_with_paging(chevy_volt):
    permissions = chevy_volt.permissions({"limit": 1, "offset": 1})
    assert permissions is not None
    assert type(permissions) == types.Permissions
    assert permissions._fields == ("permissions", "paging", "meta")
    assert permissions.paging.count == len(ah.DEFAULT_SCOPE)
    assert permissions.paging.offset == 1


def test_webhooks(chevy_volt):
    if ah.APPLICATION_MANAGEMENT_TOKEN:
        if ah.WEBHOOK_ID is None:
            raise Exception(
                "To test webhooks, you must export 'E2E_SMARTCAR_AMT' and 'E2E_SMARTCAR_WEBHOOK_ID' as"
                "environment variables."
            )

        subscribe = chevy_volt.subscribe(ah.WEBHOOK_ID)

        assert subscribe is not None
        assert type(subscribe) == types.Subscribe
        assert subscribe._fields == ("webhook_id", "vehicle_id", "meta")

        unsubscribe = chevy_volt.unsubscribe(
            ah.APPLICATION_MANAGEMENT_TOKEN, ah.WEBHOOK_ID
        )
        assert unsubscribe is not None
        assert type(unsubscribe) == types.Status
        assert unsubscribe._fields == ("status", "meta")


def test_request(chevy_volt):
    odometer = chevy_volt.request(
        "GET", "odometer", None, {"sc-unit-system": "imperial"}
    )
    assert type(odometer) == types.Response
    assert odometer.body is not None
    assert isinstance(odometer.meta, tuple)
    assert odometer._fields == ("body", "meta")
    assert odometer.meta.unit_system == "imperial"


def test_request_override_header(chevy_volt):
    try:
        chevy_volt.request(
            "GET",
            "odometer",
            None,
            {
                "sc-unit-system": "imperial",
                "Authorization": "Bearer abc",
            },
        )
    except SmartcarException as sc_e:
        assert (
            sc_e.message
            == "AUTHENTICATION - The authorization header is missing or malformed, or it contains invalid or expired authentication credentials. Please check for missing parameters, spelling and casing mistakes, and other syntax issues."
        )


def test_request_with_body(chevy_volt):
    batch = chevy_volt.request(
        "post",
        "batch",
        {"requests": [{"path": "/odometer"}, {"path": "/tires/pressure"}]},
    )
    assert type(batch) is types.Response
    assert batch.body is not None
    assert isinstance(batch.meta, tuple)
    assert batch.body["responses"][0]["path"] == "/odometer"
    assert batch.body["responses"][0]["path"] == "/odometer"
    assert batch.body["responses"][0]["code"] == 200
    assert isinstance(batch.body["responses"][0]["body"]["distance"], float)
    assert batch.body["responses"][1]["path"] == "/tires/pressure"
    assert isinstance(batch.body["responses"][1]["body"]["frontLeft"], float)
    assert isinstance(batch.body["responses"][1]["body"]["frontRight"], float)
    assert isinstance(batch.body["responses"][1]["body"]["backLeft"], float)
    assert isinstance(batch.body["responses"][1]["body"]["backRight"], float)


def test_chevy_imperial(chevy_volt_imperial):
    response = chevy_volt_imperial.odometer()
    assert response.meta.unit_system == "imperial"


def test_setting_unit_system(chevy_volt):
    chevy_volt._unit_system = "imperial"
    response = chevy_volt.odometer()
    assert response.meta.unit_system == "imperial"


def test_v1_request(chevy_volt_v1):
    odometer = chevy_volt_v1.odometer()
    assert odometer.distance is not None
    assert odometer.meta.request_id is not None


# Disconnect test MUST be at the end of the file
def test_disconnect(chevy_volt):
    disconnected = chevy_volt.disconnect()
    assert disconnected is not None
    assert type(disconnected) == types.Status
    assert disconnected._fields == ("status", "meta")
