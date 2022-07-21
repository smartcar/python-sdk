from smartcar import Vehicle


def test_vehicle_constructor():
    vid = "ada7207c-3c0a-4027-a47f-6215ce6f7b93"
    token = "9ad942c6-32b8-4af2-ada6-5e8ecdbad9c2"
    vehicle = Vehicle(
        vid,
        token,
    )
    header = vehicle._get_headers()
    assert header["Authorization"] == f"Bearer {token}"
    assert header["sc-unit-system"] == "metric"

    path = "pizza"
    test_url = vehicle._format_url(path)
    expected_url = f"https://api.smartcar.com/v2.0/vehicles/{vid}/{path}"
    assert test_url == expected_url


def test_vehicle_constructor_with_flags():
    vid = "ada7207c-3c0a-4027-a47f-6215ce6f7b93"
    token = "9ad942c6-32b8-4af2-ada6-5e8ecdbad9c2"
    vehicle = Vehicle(
        vid,
        token,
        options={"flags": {"country": "DE", "flag": True}},
    )
    header = vehicle._get_headers()
    assert header["Authorization"] == f"Bearer {token}"
    assert header["sc-unit-system"] == "metric"

    path = "pizza"
    test_url = vehicle._format_url(path)
    expected_url = f"https://api.smartcar.com/v2.0/vehicles/{vid}/{path}?flags=country:DE flag:true"
    assert test_url == expected_url


def test_vehicle_constructor_options():
    vid = "ada7207c-3c0a-4027-a47f-6215ce6f7b93"
    token = "9ad942c6-32b8-4af2-ada6-5e8ecdbad9c2"
    units_system = "imperial"
    version = "6.6"
    vehicle = Vehicle(
        vid,
        token,
        options={
            "unit_system": units_system,
            "version": version,
        },
    )
    header = vehicle._get_headers()
    assert header["Authorization"] == f"Bearer {token}"
    assert header["sc-unit-system"] == units_system

    path = "pizza"
    test_url = vehicle._format_url(path)
    expected_url = f"https://api.smartcar.com/v{version}/vehicles/{vid}/{path}"
    assert test_url == expected_url
