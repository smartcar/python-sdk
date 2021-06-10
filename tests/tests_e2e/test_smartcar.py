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
