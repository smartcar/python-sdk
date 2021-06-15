import smartcar.static as static
import tests.auth_helpers as ah


def test_correct_keys_in_access_object(access_object):
    assert access_object is not None
    assert "access_token" in access_object
    assert "token_type" in access_object
    assert "refresh_token" in access_object
    assert "expires_in" in access_object
    assert "expiration" in access_object
    assert "refresh_expiration" in access_object


def test_refresh_code(client, access_object):
    new_access_object = client.exchange_refresh_token(access_object.get("refresh_token"))
    test_correct_keys_in_access_object(new_access_object)


def test_get_compatibility(access_object, chevy_volt):
    access_token = access_object.get("access_token")
    res = static.get_compatibility(access_token, vin=chevy_volt.vin(), scope=['read_vehicle_info'],
                                   options={"client_id": ah.CLIENT_ID, "client_secret": ah.CLIENT_SECRET})

    import ipdb;
    ipdb.set_trace()
    assert "compatibility" in res
