import tests.auth_helpers as ah
import smartcar.constants as constants
import smartcar.static as static


def test_correct_attributes(api_instance, access_object, chevy_volt):
    access_token = access_object.get("access_token")
    assert api_instance.access_token == access_token
    assert api_instance.vehicle_id == chevy_volt.vehicle_id
    assert api_instance.auth == {"Authorization": f"Bearer {access_token}"}
    assert api_instance.unit_system == "metric"


def test_env_setting(api_instance):
    api_instance._set_env(testing=True)

    assert api_instance.client_id == ah.CLIENT_ID
    assert api_instance.client_secret == ah.CLIENT_SECRET


def test_set_unit_system(api_instance):
    api_instance.set_unit_system("imperial")
    assert api_instance.unit_system == "imperial"

    api_instance.set_unit_system("metric")
    assert api_instance.unit_system == "metric"


def test_format_vehicle_endpoint(api_instance, chevy_volt):
    chevy_id = chevy_volt.vehicle_id
    test_endpoint = "YAYCARS"

    test_formatted = api_instance._format_vehicle_endpoint(test_endpoint)
    expected = f"{api_instance.base_url}/vehicles/{chevy_id}/{test_endpoint}"
    expected_manual = (
        f"{constants.API_URL}/v{static.API_VERSION}/vehicles/{chevy_id}/{test_endpoint}"
    )

    assert test_formatted == expected
    assert test_formatted == expected_manual
