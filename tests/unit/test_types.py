import smartcar.types as ty


def test_generate_named_tuple():
    test_dict = {"a": True, "b": 100, "c": "apple", "hyphen-to-underscore": True}
    meta = ty.generate_named_tuple(test_dict, "Meta")

    assert meta.a
    assert meta.b == 100
    assert meta.c == "apple"
    assert meta.hyphen_to_underscore


def test_select_named_tuple_on_dict():
    mock_user_res_dict = {
        "headers": {"origin": "here", "url": "pythonsdk.testing"},
        "body": {"id": "qwerty123", "testing": True},
    }

    # Test 1 - No paths matching -> Return "body" as a dictionary (i.e. the else statement)
    test_path_1 = "TESTING"
    res1 = ty.select_named_tuple(test_path_1, mock_user_res_dict)
    assert res1.id == mock_user_res_dict["body"]["id"]
    assert res1.testing

    # Test 2 - Test against one of the predetermined paths in 'select_named_tuple'
    test_path_2 = "user"
    res2 = ty.select_named_tuple(test_path_2, mock_user_res_dict)

    assert type(res2) == ty.User
    assert res2.meta.origin == mock_user_res_dict["headers"]["origin"]
    assert res2.id == "qwerty123"
