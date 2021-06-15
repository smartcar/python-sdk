import smartcar.static as static


def test_get_user(access_object):
    access_token = access_object.get("access_token")
    res = static.get_user(access_token)

    assert "id" in res


def test_get_vehicles(access_object):
    access_token = access_object.get("access_token")
    res = static.get_vehicles(access_token)

    assert "vehicles" in res
    assert "paging" in res
