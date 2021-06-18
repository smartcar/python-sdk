import smartcar.types as ty


def test_meta():
    test_dict = {"a": True, "b": 100, "c": "apple", "hyphen-to-underscore": True}
    meta = ty.Meta(**test_dict)

    assert meta.a
    assert meta.b == 100
    assert meta.c == "apple"
    assert meta.hyphen_to_underscore


def test_batch():
    test_dict = {"a": True, "b": 100, "c": "apple"}
    batch = ty.Batch(**test_dict)

    assert batch.a
    assert batch.b == 100
    assert batch.c == "apple"


def test_select_named_tuple_on_dict():
    mock_user_res_dict = {
        "headers": {"origin": "here", "url": "pythonsdk.testing"},
        "body": {"id": "qwerty123", "testing": True},
    }

    # Test 1 - No paths matching -> Return "body" as a dictionary (i.e. the else statement)
    test_path_1 = "TESTING"
    res1 = ty.select_named_tuple(test_path_1, mock_user_res_dict)
    assert res1 == mock_user_res_dict["body"]

    # Test 2 - Test against one of the predetermined paths in 'select_named_tuple'
    test_path_2 = "user"
    res2 = ty.select_named_tuple(test_path_2, mock_user_res_dict)

    assert type(res2) == ty.User
    assert type(res2.meta) == ty.Meta
    assert res2.id == "qwerty123"
