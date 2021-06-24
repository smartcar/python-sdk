import requests.structures as rs
import smartcar.types as ty


# Tests
def test_vin_and_meta(chevy_volt):
    vin = chevy_volt.vin()
    assert vin is not None
    assert type(vin) == ty.Vin
    assert vin._fields == ("vin", "meta")
    assert type(vin.meta) == rs.CaseInsensitiveDict


def test_charge(chevy_volt):
    charge = chevy_volt.charge()
    assert charge is not None
    assert type(charge) == ty.Charge
    assert charge._fields == ("is_plugged_in", "state", "meta")
    assert charge.is_plugged_in is not None


def test_battery(chevy_volt):
    battery = chevy_volt.battery()
    assert battery is not None
    assert type(battery) == ty.Battery
    assert battery._fields == ("percent_remaining", "range", "meta")


def test_battery_capacity(chevy_volt):
    battery_capacity = chevy_volt.battery_capacity()
    assert battery_capacity is not None
    assert type(battery_capacity) == ty.BatteryCapacity
    assert battery_capacity._fields == ("capacity", "meta")


def test_fuel(chevy_volt):
    fuel = chevy_volt.fuel()
    assert fuel is not None
    assert type(fuel) == ty.Fuel
    assert fuel._fields == ("range", "percent_remaining", "amount_remaining", "meta")


def test_tire_pressure(chevy_volt):
    tire_pressure = chevy_volt.tire_pressure()
    assert tire_pressure is not None
    assert type(tire_pressure) == ty.TirePressure
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
    assert type(engine_oil) == ty.EngineOil
    assert engine_oil._fields == ("life_remaining", "meta")


def test_odometer(chevy_volt):
    odometer = chevy_volt.odometer()
    assert odometer is not None
    assert type(odometer) == ty.Odometer
    assert odometer._fields == ("distance", "meta")


def test_location(chevy_volt):
    location = chevy_volt.location()
    assert location is not None
    assert type(location) == ty.Location
    assert location._fields == ("latitude", "longitude", "meta")


def test_attributes(chevy_volt):
    attributes = chevy_volt.attributes()
    assert attributes is not None
    assert type(attributes) == ty.Attributes
    assert attributes._fields == ("id", "make", "model", "year", "meta")


def test_lock(chevy_volt):
    response = chevy_volt.lock()
    assert response.status == "success"
    assert type(response) == ty.Action
    assert response._fields == ("status", "message", "meta")


def test_unlock(chevy_volt):
    response = chevy_volt.unlock()
    assert response.status == "success"
    assert type(response) == ty.Action
    assert response._fields == ("status", "message", "meta")


def test_start_charge(vw_egolf):
    response = vw_egolf.start_charge()
    assert response.status == "success"
    assert type(response) == ty.Action
    assert response._fields == ("status", "message", "meta")


def test_stop_charge(vw_egolf):
    response = vw_egolf.stop_charge()
    assert response.status == "success"
    assert type(response) == ty.Action
    assert response._fields == ("status", "message", "meta")


def test_batch(chevy_volt):
    batch = chevy_volt.batch(["/odometer", "/location"])
    assert batch is not None
    assert batch._fields == ("odometer", "location", "meta")

    # assert meta and nested meta types
    assert type(batch.meta) == rs.CaseInsensitiveDict
    assert type(batch.odometer.meta) == rs.CaseInsensitiveDict


def test_permissions(chevy_volt):
    permissions = chevy_volt.permissions()
    assert permissions is not None
    assert type(permissions) == ty.Permissions
    assert permissions._fields == ("permissions", "meta")


def test_batch_and_set_unit_system(chevy_volt):
    chevy_volt.set_unit_system("imperial")
    batch = chevy_volt.batch(["/odometer", "/fuel"])
    assert batch.odometer.meta.get("sc-unit-system") == "imperial"


def test_disconnect(chevy_volt):
    disconnected = chevy_volt.disconnect()
    assert disconnected is not None
    assert type(disconnected) == ty.Status
    assert disconnected._fields == ("status", "meta")
