import smartcar
from smartcar import get_user
from smartcar.exception import SmartcarException, exception_factory


def test_wrong_access_token():
    bad_token = "THIS_SHOULD_NOT_WORK"
    try:
        res = get_user(bad_token)
    except Exception as e:
        assert isinstance(e, SmartcarException)


def test_wrong_vehicle_id(vw_egolf):
    try:
        vw_egolf.odometer()
    except Exception as e:
        assert isinstance(e, SmartcarException)

        # 8 fields stated in exception.py + 'message'
        assert len(e.__dict__.keys()) == 9
        assert e.status_code == 403


def test_v1_exception(access_vw, vw_egolf):
    try:
        vw_egolf_for_v1_api = smartcar.Vehicle(
            vw_egolf.vehicle_id, access_vw.access_token, {"version": "1.0"}
        )
        vw_egolf_for_v1_api.odometer()
    except Exception as e:
        assert len(e.__dict__.keys()) == 5
        assert e.status_code == 403


def test_non_json_exception():
    try:
        exception_factory(100, {"Content-Type": "weird"}, "Yay")
    except Exception as e:
        assert e.message == "Yay"
        assert e.status_code == 100
        assert len(e.__dict__.keys()) == 2
