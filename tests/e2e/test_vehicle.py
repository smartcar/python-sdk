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


def test_get_charge_limit(ford_car):
    charge_limit = ford_car.get_charge_limit()
    assert charge_limit is not None
    assert type(charge_limit) == types.ChargeLimit
    assert charge_limit._fields == ("limit", "meta")


def test_lock_status(chevy_volt):
    lock_status = chevy_volt.lock_status()
    assert lock_status is not None
    assert type(lock_status) == types.LockStatus
    assert lock_status._fields == (
        "is_locked",
        "doors",
        "windows",
        "sunroof",
        "storage",
        "charging_port",
        "meta",
    )


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


def test_set_charge_limit(ford_car):
    response = ford_car.set_charge_limit(0.7)
    assert response.status == "success"
    assert type(response) == types.Action
    assert response._fields == ("status", "message", "meta")


def test_send_destination(ford_car):
    # The latitude and longitude of the Empire State Building in New York, USA.
    response = ford_car.send_destination(40.748817, -73.985428)
    assert response.status == "success"
    assert type(response) == types.Action
    assert response._fields == ("status", "message", "meta")


def test_service_history(ford_car):
    response = ford_car.service_history("2023-05-20", "2024-02-10")
    assert isinstance(
        response, types.ServiceHistory
    ), "Response should be an instance of ServiceHistory"
    assert hasattr(response, "_fields"), "Response should have '_fields' attribute"
    assert "items" in response._fields, "'items' should be a key in the response fields"

    # Check the 'items' array.
    assert isinstance(response.items, list), "Items should be a list"

    # Iterate over each item in the 'items' list to perform further validations.
    for item in response.items:
        assert isinstance(
            item["odometerDistance"], (float, int)
        ), "Odometer distance should be a numeric type (float or int)"
        assert (
            item["odometerDistance"] > 0
        ), "Odometer distance should be greater than zero"

    assert response._fields == ("items", "meta")


def test_diagnostic_system_status(ford_car):
    diagnostic_status = ford_car.diagnostic_system_status()
    assert diagnostic_status is not None
    assert type(diagnostic_status) == types.DiagnosticSystemStatus
    assert diagnostic_status._fields == ("systems", "meta")
    
    systems = [types.DiagnosticSystem(**s) if isinstance(s, dict) else s for s in diagnostic_status.systems]
    for system in systems:
        assert isinstance(system, types.DiagnosticSystem)



def test_diagnostic_trouble_codes(ford_car):
    dtc_response = ford_car.diagnostic_trouble_codes()
    assert dtc_response is not None
    assert type(dtc_response) == types.DiagnosticTroubleCodes
    assert dtc_response._fields == ("active_codes", "meta")
    
    active_codes = [types.DiagnosticTroubleCode(**c) if isinstance(c, dict) else c for c in dtc_response.active_codes]
    for code in active_codes:
        assert isinstance(code, types.DiagnosticTroubleCode)



def test_batch_diagnostics(ford_car):
    batch_response = ford_car.batch(["/diagnostics/system_status", "/diagnostics/dtcs"])
    assert batch_response is not None
    assert batch_response._fields == ("diagnostic_system_status", "diagnostic_trouble_codes", "meta")
    
    diagnostic_status = batch_response.diagnostic_system_status()
    assert diagnostic_status is not None
    systems = [types.DiagnosticSystem(**s) if isinstance(s, dict) else s for s in diagnostic_status.systems]
    for system in systems:
        assert isinstance(system, types.DiagnosticSystem)
    
    trouble_codes = batch_response.diagnostic_trouble_codes()
    assert trouble_codes is not None
    active_codes = [types.DiagnosticTroubleCode(**c) if isinstance(c, dict) else c for c in trouble_codes.active_codes]
    for code in active_codes:
        assert isinstance(code, types.DiagnosticTroubleCode)



def test_batch_success(chevy_volt):
    batch = chevy_volt.batch(
        [
            "/odometer",
            "/location",
            "/charge/limit",
            "/engine/oil",
            "/battery/capacity",
            "/tires/pressure",
        ]
    )
    assert batch is not None
    assert batch._fields == (
        "odometer",
        "location",
        "get_charge_limit",
        "engine_oil",
        "battery_capacity",
        "tire_pressure",
        "meta",
    )
    assert isinstance(batch.meta, tuple)
    assert isinstance(batch.odometer().meta, tuple)
    assert batch.odometer().distance is not None
    assert batch.odometer().meta.request_id is not None
    assert batch.location().longitude is not None
    assert batch.location().latitude is not None
    assert batch.location().meta.request_id is not None
    assert batch.get_charge_limit().limit is not None
    assert batch.engine_oil().life_remaining is not None
    assert batch.battery_capacity().capacity is not None
    assert batch.tire_pressure().front_right is not None
    assert batch.tire_pressure().front_left is not None
    assert batch.tire_pressure().back_right is not None
    assert batch.tire_pressure().back_left is not None


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
