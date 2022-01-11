import smartcar.auth_client as ac
import urllib.parse as urlparse


def test_correct_keys_in_access_object(access):
    access_object = access._asdict()
    assert "access_token" in access_object
    assert "token_type" in access_object
    assert "refresh_token" in access_object
    assert "expires_in" in access_object
    assert "expiration" in access_object
    assert "refresh_expiration" in access_object


def test_refresh_code_with_flag(client, access):
    new_access_object = client.exchange_refresh_token(
        access.refresh_token, {"test_flag": True}
    )
    test_correct_keys_in_access_object(new_access_object)


def test_auth_client(client):
    assert client.client_id is not None
    assert client.client_secret is not None
    assert client.redirect_uri is not None
    assert client.test_mode


def test_get_auth_url_single_select(client):
    options = {"single_select": {"enabled": True}}

    test_url_ss_enabled = client.get_auth_url(
        ["read_odometer", "read_vehicle_info"], options
    )
    query_params = urlparse.parse_qs(test_url_ss_enabled)
    assert query_params["single_select"][0] == "true"

    # Testing the explicit setting of single_select to false:
    options_2 = {"single_select": {"enabled": False}}
    test_url_ss_disabled = client.get_auth_url(
        ["read_odometer", "read_vehicle_info"], options_2
    )
    query_params_2 = urlparse.parse_qs(test_url_ss_disabled)
    assert query_params_2["single_select"][0] == "false"


def test_set_expiration(access):
    access_object = access._asdict()
    access_object.pop("expiration")
    access_object.pop("refresh_expiration")
    assert "expiration" not in access_object
    assert "refresh_expiration" not in access_object

    ac._set_expiration(access_object)
    assert "expiration" in access_object
    assert "refresh_expiration" in access_object
