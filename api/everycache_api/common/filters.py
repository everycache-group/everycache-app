import operator
from functools import partial

from flask import request
from marshmallow import Schema
from marshmallow.exceptions import ValidationError
from sqlalchemy.orm import Query


def _like_operator_helper(model_field, value: str, like: bool = True):
    return (model_field.like if like else model_field.notlike)(f"%{value}%")


def apply_query_filters(query: Query, schema: Schema) -> Query:
    operations = {
        "": operator.eq,
        "lte": operator.le,
        "lt": operator.lt,
        "gte": operator.ge,
        "gt": operator.gt,
        "not": operator.ne,
        "like": _like_operator_helper,
        "not-like": partial(_like_operator_helper, like=False),
    }

    args = request.args.to_dict(flat=False)

    for field_name, filters in args.items():
        if field_name not in schema.fields:
            # skip incorrect/illegal fields
            continue

        schema_field = schema.fields[field_name]

        if schema_field.load_only:
            # skip load_only fields
            continue

        if schema_field.data_key or schema_field.attribute:
            # skip fields with different name in database model, eg. id/ext_id
            continue

        db_model_field = getattr(schema.Meta.model, field_name)

        for filter_string in filters:
            if ":" in filter_string:
                # pattern: <field>=<operation>:<value>
                operation_str, value = filter_string.split(":")
            else:
                # pattern: <field>=<value>
                operation_str, value = "", filter_string

            operation = operations.get(operation_str)

            if not operation:
                continue

            try:
                schema_field.deserialize(value)
            except ValidationError:
                continue

            query = query.filter(operation(db_model_field, value))

    return query
