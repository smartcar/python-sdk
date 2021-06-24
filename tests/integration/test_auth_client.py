import smartcar.auth_client as ac
import urllib.parse as urlparse
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
    new_access_object = client.exchange_refresh_token(
        access_object.get("refresh_token")
    )
    test_correct_keys_in_access_object(new_access_object)


def test_auth_client(client):
    assert client.client_id is not None
    assert client.client_secret is not None
    assert client.redirect_uri is not None
    assert client.test_mode


def test_get_auth_url_with_options(client):
    options = {
        "force_prompt": True,
        "state": "WEEEEEEEEE",
        "make_bypass": "Ford",
        "single_select": {"enabled": True, "vin": "abcdefghi12345678"},
        "flags": {"flag_1": "Yay", "flag_2": True, "flag_3": 123},
    }

    test_url = client.get_auth_url(["read_odometer", "read_vehicle_info"], options)
    query_params = urlparse.parse_qs(test_url)

    assert query_params["client_id"][0] == ah.CLIENT_ID
    assert query_params["redirect_uri"][0] == ah.REDIRECT_URI
    assert query_params["approval_prompt"][0] == "force"
    assert query_params["scope"][0] == "read_odometer read_vehicle_info"
    assert query_params["mode"][0] == "test"
    assert query_params["state"][0] == "WEEEEEEEEE"
    assert query_params["make"][0] == "Ford"
    assert query_params["single_select"][0] == "True"
    assert query_params["single_select_vin"][0] == "abcdefghi12345678"
    assert query_params["flags"][0] == "flag_1:Yay flag_2:True flag_3:123"


def test_set_expiration(access_object):
    access_object.pop("expiration")
    access_object.pop("refresh_expiration")
    assert "expiration" not in access_object
    assert "refresh_expiration" not in access_object

    ac._set_expiration(access_object)
    assert "expiration" in access_object
    assert "refresh_expiration" in access_object
