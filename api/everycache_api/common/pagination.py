"""Simple helper to paginate query"""
from flask import request, url_for

from everycache_api.common.filters import apply_query_filters
from everycache_api.common.ordering import apply_query_ordering

DEFAULT_PAGE_SIZE = 50
DEFAULT_PAGE_NUMBER = 1


def extract_pagination(page=None, per_page=None, **request_args):
    page = int(page) if page is not None else DEFAULT_PAGE_NUMBER
    per_page = int(per_page) if per_page is not None else DEFAULT_PAGE_SIZE
    return page, per_page, request_args


def paginate(query, schema):
    query = apply_query_ordering(query, schema)
    query = apply_query_filters(query, schema)

    page, per_page, other_request_args = extract_pagination(**request.args)
    page_obj = query.paginate(page=page, per_page=per_page)
    next_ = (
        url_for(
            request.endpoint,
            page=page_obj.next_num,
            per_page=per_page,
            **other_request_args,
            **request.view_args,
        )
        if page_obj.has_next
        else False
    )
    prev = (
        url_for(
            request.endpoint,
            page=page_obj.prev_num,
            per_page=per_page,
            **other_request_args,
            **request.view_args,
        )
        if page_obj.has_prev
        else False
    )

    return {
        "total": page_obj.total,
        "pages": page_obj.pages,
        "next": next_,
        "prev": prev,
        "results": schema.dump(page_obj.items),
    }
