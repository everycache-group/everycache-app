from collections import OrderedDict
from datetime import datetime
from types import SimpleNamespace

import pytest
from marshmallow import fields

from everycache_api.common.filters import apply_query_filters


@pytest.fixture()
def prepare_mocks(app, mocker):
    query_mock = mocker.MagicMock()
    schema_mock = mocker.MagicMock()

    with app.test_request_context():
        request_mock = mocker.patch("everycache_api.common.filters.request")

    operator_mock = mocker.patch("everycache_api.common.filters.operator")
    request_mock.args.to_dict = mocker.MagicMock()
    query_mock.filter = mocker.MagicMock()

    return (
        query_mock, schema_mock, request_mock, operator_mock
    )


class TestFilters:

    @pytest.fixture()
    def mocks(self, prepare_mocks):
        mocks = SimpleNamespace()
        (mocks.query_mock, mocks.schema_mock, mocks.request_mock,
         mocks.operator_mock) = prepare_mocks
        return mocks

    happy_path_filters = (
        ("field_name_1", "eq", "dominik"),
        ("field_name_2", "gt", 3),
        ("field_name_3", "ge", 2),
        ("field_name_4", "lt", 2),
        ("field_name_5", "le", 3),
        ("field_name_6", "ne", "asdf"),
        ("field_name_7", "like", "asdf"),
        ("field_name_8", "notlike", "asdf"),
    )

    def _get_mocks_for_filters(self, filters, mocker):
        field_mocks = {}
        model_mocks = {}
        for field_name, *_ in filters:
            schema_field_mock = mocker.MagicMock()
            model_mock = mocker.MagicMock()
            schema_field_mock.data_key = False
            schema_field_mock.load_only = False
            schema_field_mock.attribute = False
            field_mocks[field_name] = schema_field_mock
            model_mocks[field_name] = model_mock
        return field_mocks, model_mocks

    def _get_filter_args(self, filters):
        operator_name_mapping = {"ge": "gte", "le": "lte", "ne": "not",
                                       "notlike": "not-like"}
        filter_args = OrderedDict()
        for field_name, operator_name, value in filters:
            query_operator_name = operator_name_mapping.get(
                operator_name, operator_name)

            value_string = str(value)
            if operator_name != "eq":
                value_string = f"{query_operator_name}:{value}"

            filter_args[field_name] = [value_string]

        return filter_args

    def _get_params(self, filters, mocks, field_mocks, model_mocks):
        params = {}
        for field_name, operator_name, value in filters:
            operator_source = mocks.operator_mock
            if operator_name in ("like", "notlike"):
                operator_source = model_mocks[field_name]

            operator = getattr(operator_source, operator_name)
            param = operator(field_mocks[field_name], value)
            params[field_name] = param

        return params

    def test_filters_happy_path(self, mocks, mocker):
        field_mocks, model_mocks = self._get_mocks_for_filters(
            self.happy_path_filters, mocker)

        mocks.schema_mock.fields = dict(field_mocks)
        for field_name, model_mock in model_mocks.items():
            setattr(mocks.schema_mock.Meta.model, field_name, model_mock)

        mocks.request_mock.args.to_dict.return_value = self._get_filter_args(
            self.happy_path_filters)

        result = apply_query_filters(mocks.query_mock, mocks.schema_mock)

        params = self._get_params(self.happy_path_filters, mocks, field_mocks,
                                  model_mocks)

        for field_name, *_ in self.happy_path_filters:
            param = params[field_name]
            mocks.query_mock.filter.assert_called_once_with(param)
            mocks.query_mock = mocks.query_mock.filter(param)

        assert result == mocks.query_mock
