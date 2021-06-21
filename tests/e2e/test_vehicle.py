# Tests
def test_vin(chevy_volt):
    vin = chevy_volt.vin()
    assert vin is not None


def test_charge(chevy_volt):
    charge = chevy_volt.charge()
    assert charge is not None


def test_battery(chevy_volt):
    battery = chevy_volt.battery()
    assert battery is not None


def test_battery_capacity(chevy_volt):
    battery = chevy_volt.battery_capacity()
    assert battery is not None


def test_fuel(chevy_volt):
    fuel = chevy_volt.fuel()
    assert fuel is not None


def test_tire_pressure(chevy_volt):
    tire_pressure = chevy_volt.tire_pressure()
    assert tire_pressure is not None


def test_oil(chevy_volt):
    oil = chevy_volt.oil()
    assert oil is not None


def test_odometer(chevy_volt):
    odometer = chevy_volt.odometer()
    assert odometer is not None


def test_location(chevy_volt):
    location = chevy_volt.location()
    assert location is not None


def test_info(chevy_volt):
    info = chevy_volt.info()
    assert info is not None


def test_lock(chevy_volt):
    lock = chevy_volt.lock()
    assert lock.status == "success"


def test_unlock(chevy_volt):
    unlock = chevy_volt.unlock()
    assert unlock.status == "success"


def test_start_charge(vw_egolf):
    response = vw_egolf.start_charge()
    assert response.status == "success"


def test_stop_charge(vw_egolf):
    response = vw_egolf.stop_charge()
    assert response.status == "success"


def test_batch(chevy_volt):
    batch = chevy_volt.batch(["/odometer", "/location"])
    assert batch is not None


def test_permissions(chevy_volt):
    permissions = chevy_volt.permissions()
    assert permissions is not None


def test_batch_and_set_unit_system(chevy_volt):
    chevy_volt.set_unit_system("imperial")
    batch = chevy_volt.batch(["/odometer", "/fuel"])
    assert batch.odometer.meta.sc_unit_system == "imperial"


def test_disconnect(chevy_volt):
    disconnected = chevy_volt.disconnect()
    assert disconnected is not None