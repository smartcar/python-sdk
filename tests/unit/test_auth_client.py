import urllib.parse as urlparse
import tests.auth_helpers as ah


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
    assert query_params["single_select"][0] == "true"
    assert query_params["single_select_vin"][0] == "abcdefghi12345678"
    assert query_params["flags"][0] == "flag_1:Yay flag_2:True flag_3:123"


def test_get_auth_url_without_options(client):
    test_url = client.get_auth_url(["read_odometer", "read_vehicle_info"])
    query_params = urlparse.parse_qs(test_url)
    assert query_params["client_id"][0] == ah.CLIENT_ID
    assert query_params["redirect_uri"][0] == ah.REDIRECT_URI
    assert query_params["approval_prompt"][0] == "auto"
    assert query_params["scope"][0] == "read_odometer read_vehicle_info"
