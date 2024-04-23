import smartcar
import smartcar.smartcar
from smartcar.smartcar import get_user
from smartcar.exception import SmartcarException, exception_factory


def test_bad_access_code_exchange(client):
    """
    OAuth Error
    """
    try:
        client.exchange_code("THIS_SHOULD_NOT_WORK")
    except Exception as e:
        assert isinstance(e, SmartcarException)
        assert e.status_code == 400
        assert e.message == "Invalid code: THIS_SHOULD_NOT_WORK."


def test_bad_refresh_token_exchange(client):
    try:
        client.exchange_refresh_token("THIS_SHOULD_NOT_WORK")
    except Exception as e:
        assert isinstance(e, SmartcarException)
        assert e.status_code == 400
        assert e.message == "Invalid refresh_token: THIS_SHOULD_NOT_WORK."


def test_bad_access_token_api():
    bad_token = "THIS_SHOULD_NOT_WORK"
    try:
        get_user(bad_token)
    except Exception as e:
        assert e.detail is None
        assert isinstance(e, SmartcarException)
        assert type(e.resolution) == dict
        assert "type" in e.resolution.keys() and "url" in e.resolution.keys()


def test_vehicle_state_error(access):
    """
    resolution is None
    """
    vehicle_wrong_id = smartcar.Vehicle("bad_id", access.access_token)
    try:
        vehicle_wrong_id.attributes()
    except Exception as e:
        assert e.resolution == {"type": None, "url": None}
        assert e.status_code == 400


def test_vehicle_state_error_v1(access):
    """
    No resolution attribute
    """
    vehicle_wrong_id = smartcar.Vehicle(
        "bad_id", access.access_token, {"version": "1.0"}
    )
    try:
        vehicle_wrong_id.attributes()
    except Exception as e:
        assert e.type == "validation_error"
        assert "resolution" not in e.__dict__


def test_out_of_permission_scope(ford_car):
    """
    status code: 403, no "error" code
    """
    try:
        ford_car.odometer()
    except Exception as e:
        assert isinstance(e, SmartcarException)

        # 9 fields stated in exception.py + 'message'
        assert len(e.__dict__.keys()) == 10
        assert e.status_code == 403
        assert e.code is None

        # message formatted correctly (i.e. without colon: <code>)
        assert e.message[:13] == "PERMISSION - "
        assert "type" in e.resolution.keys() and "url" in e.resolution.keys()


def test_out_of_permission_scope_v1(access_ford, ford_car):
    """
    v1 permission error, code is None
    """
    try:
        smartcar.set_api_version("1.0")
        tesla_for_v1_api = smartcar.Vehicle(
            ford_car.vehicle_id, access_ford.access_token
        )
        tesla_for_v1_api.odometer()
    except Exception as e:
        assert e.code is None
        assert len(e.__dict__.keys()) == 5
        assert e.status_code == 403
    finally:
        smartcar.set_api_version("2.0")
        smartcar.set_api_version(smartcar.smartcar.API_VERSION)


def test_set_unit_system_value_error(chevy_volt):
    try:
        chevy_volt.set_unit_system("MeTriC")
        assert chevy_volt._unit_system == "metric"

        chevy_volt.set_unit_system("ImPeriMEtric")
    except Exception as e:
        assert type(e) == ValueError
        assert chevy_volt._unit_system == "metric"


def test_vehicle_bad_api_version(chevy_volt):
    try:
        # Smartcar API will default to latest version number, so long
        # as version follows the format "\d+\.\d+"
        chevy_volt._api_version = "99999999.99"
        res = chevy_volt.odometer()
        assert res.distance is not None

        # This, however, should result in an error
        chevy_volt._api_version = "Johnny Appleseed"
        chevy_volt.odometer()
    except Exception as e:
        assert e.status_code == 404
    finally:
        chevy_volt._api_version = smartcar.smartcar.API_VERSION


def test_non_json_exception():
    try:
        raise exception_factory(100, {"Content-Type": "weird"}, "Yay")
    except Exception as e:
        assert e.message == "Yay"
        assert e.status_code == 100
        assert len(e.__dict__.keys()) == 2


def test_json_cant_be_parsed():
    """
    body string, json parse failure (SDK ERROR)
    """
    try:
        raise exception_factory(900, {"Content-Type": "application/json"}, "diggity")
    except Exception as e:
        assert isinstance(e, SmartcarException)
        assert e.message == "diggity"
        assert e.status_code == 900
        assert e.type == "SDK_ERROR"


def test_retry_after_found():
    """
    test that we can get the retry_after amount
    """
    try:
        raise exception_factory(
            429,
            {"Retry-After": 5000, "Content-Type": "application/json"},
            '{"statusCode":429,"type":"RATE_LIMIT","code":"Vehicle","resolution":{"type":"RETRY_LATER"},"requestId":"e0027f5f-4411-4247-a54d-e34c157d84c1"}',
        )
    except Exception as e:
        assert isinstance(e, SmartcarException)
        assert e.retry_after == 5000

def test_suggested_user_message():
    """
    test that we can get the retry_after amount
    """
    try:
        raise exception_factory(
            429,
            {"Retry-After": 5000, "Content-Type": "application/json"},
            '{"statusCode":429,"type":"RATE_LIMIT","code":"Vehicle","resolution":{"type":"RETRY_LATER"},"requestId":"e0027f5f-4411-4247-a54d-e34c157d84c1", "suggestedUserMessage": "Please try again later."}',
        )
    except Exception as e:
        assert isinstance(e, SmartcarException)
        assert e.suggested_user_message == "Please try again later."
