from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from everycache_api.api.schemas import CacheDetailsSchema, CacheSchema
from everycache_api.common.pagination import paginate
from everycache_api.extensions import db, jwt, ma
from everycache_api.models import Cache, User


class CacheResource(Resource):
    """Single object resource

    ---
    get:
      tags:
        - api
      parameters:
        - in: path
          name: id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  cache: CacheSchema
        404:
          description: cache does not exist
      security: []
    """

    method_decorators = [jwt_required(optional=True)]

    def get(self, id: int):
        identity = get_jwt_identity()

        if identity:
            print(identity)

        schema = CacheSchema()
        cache = Cache.query.filter_by(id_=id).first_or_404()

        return {"cache": schema.dump(cache)}


class CacheList(Resource):
    """Multiple objects resource

    ---
    get:
      tags:
        - api
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
                          $ref: '#/components/schemas/CacheSchema'
    """

    def get(self):
        schema = CacheSchema(many=True)
        query = Cache.query

        return paginate(query, schema)
