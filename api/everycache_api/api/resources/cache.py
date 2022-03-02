from flask import abort, request
from flask_jwt_extended import current_user, jwt_required
from flask_restful import Resource

from everycache_api.api.schemas import (
    CacheCommentSchema,
    CachePublicSchema,
    CacheSchema,
    CacheVisitSchema,
)
from everycache_api.common.pagination import paginate
from everycache_api.extensions import db
from everycache_api.models import Cache, CacheComment, CacheVisit, User


class CacheResource(Resource):
    """Single object resource

    ---
    get:
      tags:
        - api
      parameters:
        - in: path
          name: cache_id
          schema:
            type: string
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  cache:
                    oneOf:
                      - CacheSchema
                      - CachePublicSchema
        404:
          description: cache not found
      security: []
    put:
      tags:
        - api
      parameters:
        - in: path
          name: cache_id
          schema:
            type: string
      requestBody:
        content:
          application/json:
            schema:
              CacheSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: Cache updated.
                  cache:
                    CacheSchema
        403:
          description: forbidden
        404:
          description: cache not found
    delete:
      tags:
        - api
      parameters:
        - in: path
          name: cache_id
          schema:
            type: string
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: Cache deleted.
        403:
          description: forbidden
        404:
          description: cache not found
    """

    method_decorators = {
        "get": [jwt_required(optional=True)],
        "put": [jwt_required()],
        "delete": [jwt_required()],
    }

    def get(self, cache_id: str):
        # find cache details
        cache = Cache.query_ext_id(cache_id).first_or_404()

        # decide which schema to use
        schema = None
        if current_user:
            # logged in user
            schema = CacheSchema()
            schema.context = {"current_user": current_user}
        else:
            # guest user
            schema = CachePublicSchema()

        # return cache details
        return {"cache": schema.dump(cache)}

    def put(self, cache_id: int):
        # find cache
        cache = Cache.query_ext_id(cache_id).first_or_404()

        # ensure current_user is authorized
        if current_user != cache.owner and current_user.role != User.Role.Admin:
            abort(403, "Unauthorized to modify other users' caches.")

        schema = CacheSchema(exclude=["visited"])

        # update and return cache details
        cache = schema.load(request.json, instance=cache, partial=True)
        db.session.commit()

        # schema.context = {"current_user": current_user}

        return {"message": "Cache updated.", "cache": schema.dump(cache)}, 200

    def delete(self, cache_id: int):
        # find cache
        cache = Cache.query_ext_id(cache_id).first_or_404()

        # ensure current_user is authorized
        if current_user != cache.owner and current_user.role != User.Role.Admin:
            abort(403, "Unauthorized to delete other users' caches.")

        # mark cache as deleted
        cache.deleted = True
        db.session.commit()

        return {"message": "Cache deleted."}, 200


class CacheListResource(Resource):
    """Multiple objects resource

    ---
    get:
      tags:
        - api
      parameters:
        - in: query
          name: order_by
          schema:
            type: string
          required: false
          description: which field to order results by
        - in: query
          name: desc
          schema:
            type: boolean
          allowEmptyValue: true
          required: false
          description: order results descending
      responses:
        200:
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/PaginatedResult'
                  - type: object
                    properties:
                      results:
                        type: array
                        items:
                          oneOf:
                            - $ref: '#/components/schemas/CachePublicSchema'
                            - $ref: '#/components/schemas/CacheSchema'
      security: []
    post:
      tags:
        - api
      requestBody:
        content:
          application/json:
            schema:
              CacheSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: Cache created.
                  cache:
                    CacheSchema
        400:
          description: bad request payload
        403:
          description: forbidden
    """

    method_decorators = {"get": [jwt_required(optional=True)], "post": [jwt_required()]}

    def get(self):
        # retrieve multiple caches' info
        query = Cache.query.filter_by(deleted=False)

        # decide which schema to use
        schema = None
        if current_user:
            # logged in user
            schema = CacheSchema(many=True)
            schema.context = {"current_user": current_user}
        else:
            # guest user
            schema = CachePublicSchema(many=True)

        return paginate(query, schema)

    def post(self):
        # creating a new cache

        schema = CacheSchema(exclude=["visited"])
        cache = schema.load(request.json)

        # append current_user as owner to newly created cache
        cache.owner = current_user

        db.session.add(cache)
        db.session.commit()

        return {"message": "Cache created.", "cache": schema.dump(cache)}, 201


class CacheVisitListResource(Resource):
    """Multiple objects resource

    ---
    get:
      tags:
        - api
      parameters:
        - in: path
          name: cache_id
          schema:
            type: string
        - in: query
          name: order_by
          schema:
            type: string
          required: false
          description: field to order items by
        - in: query
          name: desc
          schema:
            type: boolean
          allowEmptyValue: true
          required: false
          description: order results descending
      responses:
        200:
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/PaginatedResult'
                  - type: object
                    properties:
                      results:
                        type: array
                        items:
                          $ref: '#/components/schemas/CacheVisitSchema'
        404:
          description: cache not found
      security: []
    post:
      tags:
        - api
      parameters:
        - in: path
          name: cache_id
          schema:
            type: string
      requestBody:
        content:
          application/json:
            schema:
              CacheVisitSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: Cache visit created.
                  cache:
                    CacheVisitSchema
        400:
          description: bad request
        403:
          description: forbidden
        404:
          description: cache not found
    """

    method_decorators = {"post": [jwt_required()]}

    def get(self, cache_id):
        # ensure cache with given id exists
        cache = Cache.query_ext_id(cache_id).first_or_404()

        schema = CacheVisitSchema(many=True)
        query = CacheVisit.query.filter_by(cache=cache)

        # list visits for cache
        return paginate(query, schema), 200

    def post(self, cache_id):
        # find cache with given id
        cache = Cache.query_ext_id(cache_id).first_or_404()

        if cache.owner == current_user:
            abort(403, "Creating a visit to own cache is forbidden.")

        # create new visit
        schema = CacheVisitSchema()
        visit = schema.load(request.json)

        # append cache and user to the visit
        visit.cache = cache
        visit.user = current_user

        # add and commit
        db.session.add(visit)
        db.session.commit()

        return {
            "message": "Cache visit created.",
            "cache_visit": schema.dump(visit),
        }, 201


class CacheCommentListResource(Resource):
    """Multiple objects resource

    ---
    get:
      tags:
        - api
      parameters:
        - in: path
          name: cache_id
          schema:
            type: string
        - in: query
          name: order_by
          schema:
            type: string
          required: false
          description: field to order items by
        - in: query
          name: desc
          schema:
            type: boolean
          allowEmptyValue: true
          required: false
          description: order results descending
      responses:
        200:
          content:
            application/json:
              schema:
                allOf:
                  - $ref '#/components/schemas/PaginatedResult'
                  - type: object
                    properties:
                      results:
                        type: array
                        items:
                          $ref: '#/components/schemas/CacheCommentSchema'
        404:
          description: cache not found
      security: []
    post:
      tags:
        - api
      parameters:
        - in: path
          name: cache_id
          schema:
            type: string
      requestBody:
        content:
          application/json:
            schema:
              CacheCommentSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: Cache comment created.
                  cache_comment:
                    CacheCommentSchema
        400:
          description: bad request
        404:
          description: cache not found
    """

    method_decorators = {"post": [jwt_required()]}

    def get(self, cache_id):
        # ensure cache with given id exists
        cache = Cache.query_ext_id(cache_id).first_or_404()

        schema = CacheCommentSchema(many=True)
        query = CacheComment.query.filter_by(cache=cache, deleted=False)

        # list comments for cache
        return paginate(query, schema), 200

    def post(self, cache_id):
        # find cache with given id
        cache = Cache.query_ext_id(cache_id).first_or_404()

        # create new comment
        schema = CacheCommentSchema()
        comment = schema.load(request.json)

        # append cache and user to the visit
        comment.cache = cache
        comment.author = current_user

        # add and commit
        db.session.add(comment)
        db.session.commit()

        return {
            "message": "Cache comment created.",
            "cache_comment": schema.dump(comment),
        }, 201
