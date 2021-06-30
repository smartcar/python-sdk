import smartcar
import smartcar.config as config
from smartcar.smartcar import get_user
from smartcar.exception import SmartcarException, exception_factory


def test_bad_access_token_exchanging_code(client):
    try:
        client.exchange_code("THIS_SHOULD_NOT_WORK")
    except Exception as e:
        assert isinstance(e, SmartcarException)
        assert e.status_code == 400
        assert e.message == "Invalid code: THIS_SHOULD_NOT_WORK."


def test_bad_access_token_api():
    bad_token = "THIS_SHOULD_NOT_WORK"
    try:
        get_user(bad_token)
    except Exception as e:
        assert isinstance(e, SmartcarException)
        assert type(e.resolution) == dict
        assert "type" in e.resolution.keys() and "url" in e.resolution.keys()


def test_out_of_permission_scope(vw_egolf):
    try:
        vw_egolf.odometer()
    except Exception as e:
        assert isinstance(e, SmartcarException)

        # 8 fields stated in exception.py + 'message'
        assert len(e.__dict__.keys()) == 9
        assert e.status_code == 403
        assert "type" in e.resolution.keys() and "url" in e.resolution.keys()


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
        chevy_volt._api_version = config.API_VERSION


def test_v1_exception(access_vw, vw_egolf):
    try:
        smartcar.set_api_version("1.0")
        vw_egolf_for_v1_api = smartcar.Vehicle(
            vw_egolf.vehicle_id, access_vw.access_token
        )
        vw_egolf_for_v1_api.odometer()
    except Exception as e:
        assert len(e.__dict__.keys()) == 5
        assert e.status_code == 403
    finally:
        smartcar.set_api_version(config.API_VERSION)


def test_non_json_exception():
    try:
        raise exception_factory(100, {"Content-Type": "weird"}, "Yay")
    except Exception as e:
        assert e.message == "Yay"
        assert e.status_code == 100
        assert len(e.__dict__.keys()) == 2
