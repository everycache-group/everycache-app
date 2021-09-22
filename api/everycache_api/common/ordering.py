from flask import request
from sqlalchemy import asc, desc

from everycache_api.extensions import ma


def apply_ordering(query, schema):
    ordering = desc if request.args.get("desc", "").lower() in ("1", "true") else asc
    order_by = request.args.get("order_by")

    if order_by:
        schema_field = schema.fields.get(order_by)

        if schema_field:
            if type(schema_field) == ma.Nested:
                # nested schema, unused for the time being
                raise NotImplementedError()
            if type(schema_field) == ma.Pluck:
                # field nested from other schema

                # join nested model to query
                nested_schema_model = schema_field.schema.Meta.model
                query = query.join(nested_schema_model)

                # apply order_by nested model's db model field to query
                nested_model_field = schema_field.field_name
                query = query.order_by(
                    ordering(getattr(nested_schema_model, nested_model_field))
                )
            else:
                # own field
                model = schema.Meta.model
                model_field = schema_field.attribute or schema_field.name

                # apply order_by
                query = query.order_by(ordering(getattr(model, model_field)))

    return query
