from flask import request
from sqlalchemy import asc, desc

from everycache_api.extensions import ma


def _query_ordering_pluck(query, schema_field, ordering):
    # join nested model to query
    nested_schema_model = schema_field.schema.Meta.model
    query = query.join(nested_schema_model)

    # apply order_by nested model's db model field to query
    nested_model_field = schema_field.field_name
    return query.order_by(ordering(getattr(nested_schema_model, nested_model_field)))


def _query_ordering_custom(query, schema, schema_field, ordering):
    # join nested model to query
    model = schema.Meta.model
    model_field = schema_field.attribute or schema_field.name

    # apply order_by
    return query.order_by(ordering(getattr(model, model_field)))


def apply_query_ordering(query, schema):
    ordering = desc if request.args.get("desc", "").lower() in ("1", "true") else asc
    order_by = request.args.get("order_by")

    if not order_by:
        return query

    schema_field = schema.fields.get(order_by)
    if not schema_field:
        return query

    if isinstance(schema_field, ma.Pluck):
        # field nested from other schema
        query = _query_ordering_pluck(query, schema_field, ordering)
    elif isinstance(schema_field, ma.Nested):
        # nested schema, unused for the time being
        raise NotImplementedError()
    else:
        # own field
        query = _query_ordering_custom(query, schema, schema_field, ordering)

    return query
