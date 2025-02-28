import smartcar.types as types
import requests.structures as rs


def test_generate_named_tuple():
    test_dict = {"a": True, "b": 100, "c": "apple", "hyphen-to-underscore": True}
    meta = types.generate_named_tuple(test_dict, "Meta", True)

    assert meta.a
    assert meta.b == 100
    assert meta.c == "apple"
    assert meta.hyphen_to_underscore


def test_select_named_tuple_on_dict():
    mock_user_res_dict = {
        "headers": {"origin": "here", "url": "testing"},
        "body": {"id": "qwerty123", "testing": True},
    }

    # Test 1 - No paths matching -> Return "body" as a dictionary (i.e. the else statement)
    test_path_1 = "TESTING"
    res1 = types.select_named_tuple(test_path_1, mock_user_res_dict)
    assert res1.id == mock_user_res_dict["body"]["id"]
    assert res1.testing

    # Test 2 - Test against one of the predetermined paths in 'select_named_tuple'
    test_path_2 = "user"
    res2 = types.select_named_tuple(test_path_2, mock_user_res_dict)

    assert type(res2) == types.User
    assert res2.id == "qwerty123"


def test_build_meta():
    headers = rs.CaseInsensitiveDict(
        {
            "sc-request-id": "36ab27d0-fd9d-4455-823a-ce30af709ffc",
            "sc-data-age": "2023-05-04T07:20:50.844Z",
            "sc-unit-system": "metric",
            "sc-fetched-at": "2023-05-04T07:20:51.844Z",
            "content-type": "application/json",
        }
    )

    meta = types.build_meta(headers)

    assert meta.request_id == "36ab27d0-fd9d-4455-823a-ce30af709ffc"
    assert meta.data_age == "2023-05-04T07:20:50.844Z"
    assert meta.unit_system == "metric"
    assert meta.fetched_at == "2023-05-04T07:20:51.844Z"

    assert not hasattr(meta, "content_type")
