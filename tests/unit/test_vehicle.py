from smartcar import Vehicle
from smartcar.exception import SmartcarException


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


def test_batch_path_response():
    path = "battery_capacity"
    path_response = {
        "code": 429,
        "path": "/battery/capacity",
        "body": {
            "statusCode": 429,
            "type": "RATE_LIMIT",
            "code": "VEHICLE",
            "description": "You have reached the throttling rate limit for this vehicle. Please see the retry-after header for when to retry the request.",
            "docURL": "https://smartcar.com/docs/errors/api-errors/rate-limit-errors#vehicle",
            "resolution": {"type": "RETRY_LATER"},
            "suggestedUserMessage": "Your vehicle is temporarily unable to connect to Optiwatt. Please be patient while we’re working to resolve this issue.",
            "requestId": "test-request-id",
        },
        "headers": {"Retry-After": 999},
    }

    top_response = {
        "responses": [path_response],
        "headers": {"Content-Type": "application/json"},
    }
    resulting_lambda = Vehicle._batch_path_response(path, path_response, top_response)

    try:
        resulting_lambda()
    except Exception as e:
        path_exception = e

    assert isinstance(path_exception, SmartcarException)
    assert path_exception.status_code == 429
    assert path_exception.request_id == "test-request-id"
    assert path_exception.type == "RATE_LIMIT"
    assert (
        path_exception.description
        == "You have reached the throttling rate limit for this vehicle. Please see the retry-after header for when to retry the request."
    )
    assert path_exception.code == "VEHICLE"
    assert path_exception.resolution == {"type": "RETRY_LATER", "url": None}
    assert path_exception.detail == None
    assert (
        path_exception.suggested_user_message
        == "Your vehicle is temporarily unable to connect to Optiwatt. Please be patient while we’re working to resolve this issue."
    )
    assert path_exception.retry_after == 999
