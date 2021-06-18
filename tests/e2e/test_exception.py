from smartcar import get_user
from smartcar.exception import SmartcarException


def test_wrong_access_token():
    bad_token = "THIS_SHOULD_NOT_WORK"
    try:
        res = get_user(bad_token)
    except Exception as e:
        assert isinstance(e, SmartcarException)
