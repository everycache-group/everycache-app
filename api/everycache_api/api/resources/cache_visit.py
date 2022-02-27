from flask import abort, request
from flask_jwt_extended import current_user, jwt_required
from flask_restful import Resource

from everycache_api.api.schemas import CacheVisitSchema
from everycache_api.extensions import db
from everycache_api.models import CacheVisit, User


class CacheVisitResource(Resource):
    """Single object resource

    ---
    get:
      tags:
        - api
      parameters:
        - in: path
          name: cache_visit_id
          schema:
            type: string
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  cache_visit: CacheVisitSchema
        404:
          description: cache visit not found
      security: []
    put:
      tags:
        - api
      parameters:
        - in: path
          name: cache_visit_id
          schema:
            type: string
      requestBody:
        content:
          application/json:
            schema:
              CacheVisitSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: Cache visit updated.
                  cache_visit: CacheVisitSchema
        403:
          description: forbidden
        404:
          description: cache visit not found
    delete:
      tags:
        - api
      parameters:
        - in: path
          name: cache_visit_id
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
                    example: Cache visit deleted.
        403:
          description: forbidden
        404:
          description: cache visit not found
    """

    method_decorators = {"put": [jwt_required()], "delete": [jwt_required()]}

    def get(self, cache_visit_id: str):
        # find and return visit
        visit = (
            CacheVisit.query_ext_id(cache_visit_id)
            .filter(CacheVisit.cache.has(deleted=False))
            .first_or_404()
        )

        schema = CacheVisitSchema()

        return {"cache_visit": schema.dump(visit)}, 200

    def put(self, cache_visit_id: str):
        # find visit
        visit = (
            CacheVisit.query_ext_id(cache_visit_id)
            .filter(CacheVisit.cache.has(deleted=False))
            .first_or_404()
        )

        # ensure current_user is authorized
        if current_user != visit.user and current_user.role != User.Role.Admin:
            abort(403, "Unauthorized to modify other users' cache visits.")

        schema = CacheVisitSchema()

        # update and return visit
        visit = schema.load(request.json, instance=visit)
        db.session.commit()

        return {
            "message": "Cache visit updated.",
            "cache_visit": schema.dump(visit),
        }, 200

    def delete(self, cache_visit_id: str):
        # find visit
        visit = CacheVisit.query_ext_id(cache_visit_id).first_or_404()

        # ensure current_user is authorized
        if current_user != visit.user and current_user.role != User.Role.Admin:
            abort(403, "Unauthorized to delete other users' cache visits.")

        # delete visit
        visit.deleted = True
        db.session.commit()

        return {"message": "Cache visit deleted."}, 200
