import pytest
from everycache_api.common.ordering import (
    apply_query_ordering,
    _query_ordering_pluck,
    _query_ordering_custom,
)
from marshmallow import fields


def _get_schema_mock(app, mocker, desc, order_by, field_type):
    schema_mock = mocker.MagicMock()
    with app.test_request_context():
        request_mock = mocker.patch("everycache_api.common.ordering.request")
    request_mock.args = {"desc": desc, "order_by": order_by}

    field_mock = mocker.MagicMock(spec=field_type)
    schema_mock.fields = {order_by: field_mock}
    return schema_mock


@pytest.mark.parametrize("desc", ("true", "false"))
@pytest.mark.parametrize("order_by", ("field1", "field2"))
@pytest.mark.parametrize("field_type", (fields.Pluck, None))
def test_apply_query_ordering(desc, order_by, field_type, app, mocker):
    query_mock = mocker.MagicMock()
    schema_mock = _get_schema_mock(app, mocker, desc, order_by, field_type)

    if field_type == fields.Pluck:
        result_mock = mocker.patch(
            "everycache_api.common.ordering._query_ordering_pluck"
        )
    else:
        result_mock = mocker.patch(
            "everycache_api.common.ordering._query_ordering_custom"
        )

    result = apply_query_ordering(query_mock, schema_mock)

    result_mock.assert_called_once()
    assert result == result_mock()


@pytest.mark.parametrize("desc", ("true", "false"))
@pytest.mark.parametrize("order_by", ("field1", "field2"))
def test_apply_query_ordering_nested(desc, order_by, app, mocker):
    query_mock = mocker.MagicMock()
    schema_mock = _get_schema_mock(app, mocker, desc, order_by, fields.Nested)

    with pytest.raises(NotImplementedError):
        apply_query_ordering(query_mock, schema_mock)


@pytest.mark.parametrize("desc", ("true", "false"))
@pytest.mark.parametrize("order_by", ("field1", "field2"))
def test_apply_query_ordering_no_model_field(desc, order_by, app, mocker):
    query_mock = mocker.MagicMock()
    schema_mock = _get_schema_mock(app, mocker, desc, order_by, fields.Nested)
    schema_mock.fields = {}

    assert apply_query_ordering(query_mock, schema_mock) == query_mock


def test_apply_query_ordering_no_order_by(app, mocker):
    query_mock = mocker.MagicMock()
    schema_mock = mocker.MagicMock()
    schema_mock.fields = {}

    with app.test_request_context():
        assert apply_query_ordering(query_mock, schema_mock) == query_mock


def test_query_ordering_pluck(mocker):
    query_mock = mocker.MagicMock()
    schema_field_mock = mocker.MagicMock()
    ordering_mock = mocker.MagicMock()

    nested_schema_model = schema_field_mock.schema.Meta.model
    nested_model_field = schema_field_mock.field_name = "field_name"

    result = _query_ordering_pluck(query_mock, schema_field_mock, ordering_mock)
    assert result == query_mock.join(nested_schema_model).order_by(
        ordering_mock(getattr(nested_schema_model, nested_model_field))
    )


def test_query_ordering_custom(mocker):
    query_mock = mocker.MagicMock()
    schema_mock = mocker.MagicMock()
    schema_field_mock = mocker.MagicMock()
    ordering_mock = mocker.MagicMock()

    model = schema_mock.Meta.model
    model_field = schema_field_mock.attribute = "attribute"

    result = _query_ordering_custom(
        query_mock, schema_mock, schema_field_mock, ordering_mock
    )
    assert result == query_mock.order_by(ordering_mock(getattr(model, model_field)))
