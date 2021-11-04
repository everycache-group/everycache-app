from datetime import datetime

from flask import request
from functools import partial
from marshmallow import fields
import operator


def _parse_value(value, schema_field_type):
    if schema_field_type == fields.Boolean:
        value = value.lower() in ("1", "true")
    elif schema_field_type == fields.Integer:
        try:
            value = int(value)
        except ValueError:
            return None
    elif schema_field_type == fields.Float:
        try:
            value = float(value)
        except ValueError:
            return None
    elif schema_field_type == fields.DateTime:
        try:
            value = datetime.strptime(value, "%d-%m-%Y")
        except ValueError:
            return None

    return value


def _like_helper(model_field, value, like=True):
    if like:
        return model_field.like(f"%{value}%")
    return model_field.notlike(f"%{value}%")


def _filter_query(query, operation_code, model_field, value):
    operations = {
        None: operator.eq,
        "lte": operator.le,
        "lt": operator.lt,
        "gte": operator.ge,
        "gt": operator.gt,
        "not": operator.ne,
        "like": _like_helper,
        "not-like": partial(_like_helper, like=False),
    }
    operation = operations.get(operation_code)
    if operation:
        query = query.filter(operation(model_field, value))

    return query


def _apply_filter(query, schema, field_name, filter_url_value):
    split_result = filter_url_value.split(":")
    try:
        operation, value_string, *_ = split_result
    except ValueError:
        operation, value_string = None, next(iter(split_result))

    schema_field_type = type(schema.fields[field_name])
    value = _parse_value(value_string, schema_field_type)
    if value is None:
        return query

    model_field = getattr(schema.Meta.model, field_name)
    return _filter_query(query, operation, model_field, value)


def apply_query_filters(query, schema):
    args = request.args.to_dict(flat=False)

    for key, values_list in args.items():
        if key not in schema.fields:
            continue

        for value in values_list:
            query = _apply_filter(query, schema, key, value)

    return query
