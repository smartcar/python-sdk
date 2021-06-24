from smartcar import get_user, Vehicle
from smartcar.exception import SmartcarException


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
