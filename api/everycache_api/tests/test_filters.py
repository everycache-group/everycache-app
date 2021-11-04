from datetime import datetime

import pytest
from marshmallow import fields

from everycache_api.common.filters import (
    _apply_filter,
    _filter_query,
    _like_helper,
    _parse_value,
    apply_query_filters,
)


class TestParseValue:

    bool_data = (
        ("1", True),
        ("true", True),
        ("True", True),
        ("", False),
        ("0", False),
        ("false", False),
        ("False", False),
        ("", False),
    )

    int_data = (
        ("lolo", None),
        ("", None),
        ("a1230", None),
        ("1230as", None),
        ("123.0", None),
        ("1", 1),
        ("120", 120),
        ("6060", 6060),
    )

    float_data = (
        ("1.0", 1.0),
        ("12.0", 12.0),
        ("2", 2.0),
        ("", None),
        ("as1.2", None),
        ("1.2as", None),
    )

    date_data = (
        ("", None),
        ("1", None),
        ("1.0", None),
        ("1-2-1997", datetime(1997, 2, 1, 0, 0)),
        ("2-3-1993", datetime(1993, 3, 2, 0, 0)),
    )

    @pytest.mark.parametrize("value, expected", bool_data)
    def test_boolean(self, value, expected):
        assert _parse_value(value, fields.Boolean) == expected

    @pytest.mark.parametrize("value, expected", int_data)
    def test_int(self, value, expected):
        assert _parse_value(value, fields.Integer) == expected

    @pytest.mark.parametrize("value, expected", float_data)
    def test_float(self, value, expected):
        assert _parse_value(value, fields.Float) == expected

    @pytest.mark.parametrize("value, expected", date_data)
    def test_date(self, value, expected):
        assert _parse_value(value, fields.DateTime) == expected


@pytest.mark.parametrize("like", (True, False))
def test_like_helper(like, mocker):
    mock = mocker.MagicMock()
    _like_helper(mock, "test_value", like)

    method_name = "like" if like else "notlike"

    getattr(mock, method_name).assert_called_once_with("%test_value%")


@pytest.mark.parametrize(
    "op_code", (None, "lte", "lt", "gte", "gt", "not", "like", "not-like")
)
def test_filter_query(op_code, mocker):
    query_mock = mocker.MagicMock()
    field_mock = mocker.MagicMock()
    dunder_method = {
        None: field_mock.__eq__,
        "lte": field_mock.__le__,
        "lt": field_mock.__lt__,
        "gte": field_mock.__gt__,
        "gt": field_mock.__ge__,
        "not": field_mock.__ne__,
        "like": field_mock.like,
        "not-like": field_mock.notlike,
    }.get(op_code)

    if op_code == "lt":
        dunder_method = field_mock.__lt__ = mocker.MagicMock()
    elif op_code == "lte":
        dunder_method = field_mock.__le__ = mocker.MagicMock()
    elif op_code == "gte":
        dunder_method = field_mock.__ge__ = mocker.MagicMock()
    elif op_code == "gt":
        dunder_method = field_mock.__gt__ = mocker.MagicMock()

    _filter_query(query_mock, op_code, field_mock, "value")

    query_mock.filter.assert_called_once()
    expected_value = "value" if op_code not in ("like", "not-like") else "%value%"
    dunder_method.assert_called_once_with(expected_value)


@pytest.mark.parametrize("field_name", ("name1", "name2", "field_name"))
@pytest.mark.parametrize("expected_parsed_value", ("val1", "val2", None))
@pytest.mark.parametrize("expected_result", ("res1", "res2"))
@pytest.mark.parametrize("url_value", ("operation:value", "value"))
def test_apply_filter(
    field_name, expected_parsed_value, expected_result, url_value, mocker
):
    query_mock = mocker.MagicMock()
    schema_mock = mocker.MagicMock()
    expected_operation = "operation" if "operation" in url_value else None
    _parse_value_mock = mocker.patch("everycache_api.common.filters._parse_value")
    _parse_value_mock.return_value = expected_parsed_value
    _filter_query_mock = mocker.patch("everycache_api.common.filters._filter_query")
    _filter_query_mock.return_value = expected_result

    result = _apply_filter(query_mock, schema_mock, field_name, url_value)

    _parse_value_mock.assert_called_once_with(
        "value", type(schema_mock.fields[field_name])
    )

    if expected_parsed_value is None:
        assert result == query_mock
    else:
        _filter_query_mock.assert_called_once_with(
            query_mock,
            expected_operation,
            getattr(schema_mock.Meta.model, field_name),
            expected_parsed_value,
        )

        assert result == expected_result


def test_apply_query_filter(app, mocker):
    query_mock = mocker.MagicMock()
    schema_mock = mocker.MagicMock()
    schema_mock.fields = ["key"]
    args = {"some_key": ["some_value"], "key": ["value"]}

    with app.test_request_context():
        request_mock = mocker.patch("everycache_api.common.filters.request")
    args_mock = request_mock.args = mocker.MagicMock()
    args_mock.to_dict.return_value = args
    request_mock.args = args_mock

    _apply_filter_mock = mocker.patch("everycache_api.common.filters._apply_filter")
    _apply_filter_mock.return_value = "query"

    result = apply_query_filters(query_mock, schema_mock)

    assert result == "query"
    _apply_filter_mock.assert_called_once_with(query_mock, schema_mock, "key", "value")
