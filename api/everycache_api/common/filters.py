import datetime

from flask import request
from marshmallow import fields


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
        value = datetime.strptime(value, "%d-%m-%y")

    return value


def _filter_query(query, operation, model_field, value):
    if operation is None:
        query = query.filter(model_field == value)
    elif operation == "lte":
        query = query.filter(model_field <= value)
    elif operation == "gte":
        query = query.filter(model_field >= value)
    elif operation == "lt":
        query = query.filter(model_field < value)
    elif operation == "gt":
        query = query.filter(model_field > value)
    elif operation == "not":
        query = query.filter(model_field != value)
    elif operation == "like":
        query = query.filter(model_field.like(f"%{value}%"))
    elif operation == "not-like":
        query = query.filter(model_field.notlike(f"%{value}%"))

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
