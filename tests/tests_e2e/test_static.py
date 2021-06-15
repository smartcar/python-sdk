import smartcar.static as static
import tests.auth_helpers as ah


def test_get_user(access_object):
    access_token = access_object.get("access_token")
    res = static.get_user(access_token)

    assert "id" in res


def test_get_vehicles(access_object):
    access_token = access_object.get("access_token")
    res = static.get_vehicles(access_token)

    assert "vehicles" in res
    assert "paging" in res


def test_get_compatibility(access_object, chevy_volt):
    access_token = access_object.get("access_token")
    res = static.get_compatibility(access_token, vin=chevy_volt.vin(), scope=['read_vehicle_info'],
                                   options={"client_id": ah.CLIENT_ID, "client_secret": ah.CLIENT_SECRET})

    assert "compatibility" in res
