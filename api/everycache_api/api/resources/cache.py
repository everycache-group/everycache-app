from flask import request
from flask_jwt_extended import current_user, jwt_required
from flask_restful import Resource

from everycache_api.api.schemas import (
    CacheCommentSchema,
    CacheSchema,
    CacheVisitSchema,
    PublicCacheSchema,
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
            type: integer
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
                      - PublicUserSchema
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
            type: integer
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
                  msg:
                    type: string
                    example: cache updated
                  cache:
                    CacheSchema
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

    def get(self, cache_id: int):
        # find cache details
        cache = Cache.query.filter_by(id_=cache_id, deleted=False).first_or_404()

        # decide which schema to use
        schema = None
        if current_user and (
            current_user == cache.owner or current_user.role == User.Role.Admin
        ):
            # owner or admin
            schema = CacheSchema()
        else:
            # default user
            schema = PublicCacheSchema()

        # return cache details
        return {"cache": schema.dump(cache)}

    def put(self, cache_id: int):
        # find cache
        cache = Cache.query.filter_by(id_=cache_id, deleted=False).first_or_404()

        # ensure current_user is authorized
        if current_user != cache.owner and current_user.role != User.Role.Admin:
            return 403

        schema = CacheSchema()

        # update and return cache details
        cache = schema.load(request.json, instance=cache)
        db.session.commit()

        return {"msg": "cache updated", "result": schema.dump(cache)}, 200

    def delete(self, cache_id: int):
        # find cache
        cache = Cache.query.filter_by(id_=cache_id, deleted=False).first_or_404()

        # ensure current_user is authorized
        if current_user != cache.owner and current_user.role != User.Role.Admin:
            return 403

        # mark cache as deleted
        cache.deleted = True
        db.session.commit()

        return {"msg": "cache deleted"}, 200


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
                            - $ref: '#/components/schemas/PublicCacheSchema'
                            - $ref: '#/components/schemas/CacheSchema'
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
                  msg:
                    type: string
                    example: cache created
                  cache:
                    CacheSchema
        400:
          description: bad request payload
    """

    method_decorators = {"get": [jwt_required(optional=True)], "post": [jwt_required()]}

    def get(self):
        # retrieve multiple caches' info
        query = Cache.query.filter_by(deleted=False)

        # decide which schema to use
        schema = None
        if current_user and current_user.role == User.Role.Admin:
            # admin
            schema = CacheSchema(many=True)
        else:
            # default user
            schema = PublicCacheSchema(many=True)

        return paginate(query, schema)

    def post(self):
        # creating a new cache

        schema = CacheSchema()
        cache = schema.load(request.json)

        # append current_user as owner to newly created cache
        cache.owner = current_user

        db.session.add(cache)
        db.session.commit()

        return {"msg": "cache created", "cache": schema.dump(cache)}, 201


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
            type: integer
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
            type: integer
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
                  msg:
                    type: string
                    example: cache visit created
                  cache:
                    CacheVisitSchema
        400:
          description: bad request
        404:
          description: cache not found
    """

    method_decorators = {"post": [jwt_required()]}

    def get(self, cache_id):
        # ensure cache with given id exists
        cache = Cache.query.filter_by(id_=cache_id, deleted=False).first_or_404()

        schema = CacheVisitSchema(many=True)
        query = CacheVisit.query.filter_by(cache=cache)

        # list visits for cache
        return paginate(query, schema), 200

    def post(self, cache_id):
        # find cache with given id
        cache = Cache.query.filter_by(id_=cache_id, deleted=False).first_or_404()

        # create new visit
        schema = CacheVisitSchema()
        visit = schema.load(request.json)

        # append cache and user to the visit
        visit.cache = cache
        visit.user = current_user

        # add and commit
        db.session.add(visit)
        db.session.commit()

        return {"msg": "cache visit created", "cache_visit": schema.dump(visit)}, 201


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
            type: integer
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
            type: integer
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
                  msg:
                    type: string
                    example: cache comment created
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
        Cache.query.filter_by(id_=cache_id, deleted=False).first_or_404()

        schema = CacheCommentSchema(many=True)
        query = CacheComment.query.filter_by(cache_id=cache_id, deleted=False)

        # list comments for cache
        return paginate(query, schema), 200

    def post(self, cache_id):
        # find cache with given id
        cache = Cache.query.filter_by(id_=cache_id, deleted=False).first_or_404()

        # create new comment
        schema = CacheCommentSchema()
        comment: CacheComment = schema.load(request.json)

        # append cache and user to the visit
        comment.cache = cache
        comment.author = current_user

        # add and commit
        db.session.add(comment)
        db.session.commit()

        return {
            "msg": "cache comment created",
            "cache_comment": schema.dump(comment),
        }, 201
