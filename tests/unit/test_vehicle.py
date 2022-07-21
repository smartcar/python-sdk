from tests.conftest import access


def test_vehicle_constructor_with_flags(chevy_volt_with_flags):
    path = "pizza"
    test_url = chevy_volt_with_flags._format_url(path)
    expected_url = f"https://api.smartcar.com/v2.0/vehicles/{chevy_volt_with_flags.vehicle_id}/{path}?flags=country:DE flag:true"
    assert test_url == expected_url
