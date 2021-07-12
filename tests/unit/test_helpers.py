import smartcar.helpers as helpers


def test_validate_env():
    assert helpers.validate_env(test_mode=True) is None


def test_format_flag_query():
    test_flags = {"flag1": True, "flag2": 100, "flag3": "apple"}
    expected_flag_str = "flag1:True flag2:100 flag3:apple"
    assert helpers.format_flag_query(test_flags) == expected_flag_str
