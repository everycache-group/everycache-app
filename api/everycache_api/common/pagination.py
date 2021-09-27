"""Simple helper to paginate query"""
from flask import request, url_for
from sqlalchemy import asc, desc

from everycache_api.extensions import ma

DEFAULT_PAGE_SIZE = 50
DEFAULT_PAGE_NUMBER = 1


def extract_pagination(page=None, per_page=None, **request_args):
    page = int(page) if page is not None else DEFAULT_PAGE_NUMBER
    per_page = int(per_page) if per_page is not None else DEFAULT_PAGE_SIZE
    return page, per_page, request_args


def apply_sorting_field(query, schema, order_by_field: str, descending: bool = False):
    field = schema.fields.get(order_by_field)
    ordering = desc if descending else asc

    if not field:
        # incorrect field
        return query
    elif type(field) == ma.Pluck:
        # nested field
        nested_schema_model = field.schema.Meta.model
        nested_model_field = field.field_name
        return query.join(nested_schema_model).order_by(
            ordering(getattr(nested_schema_model, nested_model_field))
        )
    else:
        # own field
        schema_model = schema.Meta.model
        model_field = field.attribute or field.name
        return query.order_by(ordering(getattr(schema_model, model_field)))


def paginate(query, schema):
    order_by_field = request.args.get("order_by")
    descending = request.args.get("desc", "").lower() in ("1", "true")

    if order_by_field:
        query = apply_sorting_field(query, schema, order_by_field, descending)

    # if order_by:
    #     field = schema.fields.get(order_by)
    #     if field:
    #         column = None
    #         if field.attribute is None:
    #             # schema field name equal to column name
    #             column = order_by
    #         elif "." not in field.attribute:
    #             # schema field name different than column name, but from the same object
    #             column = field.attribute
    #         else:
    #             # schema field name points to a different object in relationship
    #             relationship, column = field.attribute.split(".")
    #             db_model = getattr(schema.Meta.model, relationship).mapper.class_
    #             column = getattr(db_model, column)
    #             query = query.join(db_model)

    #         if column:
    #             # apply ordering to db query
    #             if not descending:
    #                 query = query.order_by(asc(column))
    #             else:
    #                 query = query.order_by(desc(column))

    page, per_page, other_request_args = extract_pagination(**request.args)
    page_obj = query.paginate(page=page, per_page=per_page)
    next_ = url_for(
        request.endpoint,
        page=page_obj.next_num if page_obj.has_next else page_obj.page,
        per_page=per_page,
        **other_request_args,
        **request.view_args,
    )
    prev = url_for(
        request.endpoint,
        page=page_obj.prev_num if page_obj.has_prev else page_obj.page,
        per_page=per_page,
        **other_request_args,
        **request.view_args,
    )

    return {
        "total": page_obj.total,
        "pages": page_obj.pages,
        "next": next_,
        "prev": prev,
        "results": schema.dump(page_obj.items),
    }
