from flask import request
from flask_jwt_extended import current_user, jwt_required
from flask_restful import Resource

from everycache_api.api.schemas import CacheCommentSchema
from everycache_api.extensions import db
from everycache_api.models import CacheComment, User


class CacheCommentResource(Resource):
    """Single object resource

    ---
    get:
      tags:
        - api
      parameters:
        - in: path
          name: cache_comment_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  cache_comment: CacheCommentSchema
        404:
          description: cache comment not found
      security: []
    put:
      tags:
        - api
      parameters:
        - in: path
          name: cache_comment_id
          schema:
            type: integer
      requestBody:
        content:
          application/json:
            schema:
              CacheCommentSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: cache comment updated
                  cache_comment: CacheCommentSchema
        404:
          description: cache comment not found
    delete:
      tags:
        - api
      parameters:
        - in: path
          name: cache_comment_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: cache comment deleted
        404:
          description: cache comment not found
    """

    method_decorators = {"put": jwt_required(), "delete": jwt_required()}

    def get(self, cache_comment_id):
        # find and return comment
        comment = CacheComment.query.filter_by(
            id_=cache_comment_id, deleted=False
        ).first_or_404()

        schema = CacheCommentSchema()

        return {"cache_comment": schema.dump(comment)}, 200

    def put(self, cache_comment_id):
        # find comment
        comment = CacheComment.query.filter_by(
            id_=cache_comment_id, deleted=False
        ).first_or_404()

        # ensure current_user is authorized
        if current_user != comment.author and current_user.role != User.Role.Admin:
            return 403

        schema = CacheCommentSchema()

        # update and return comment
        comment = schema.load(request.json, instance=comment)
        db.session.commit()

        return {
            "msg": "cache comment updated",
            "cache_comment": schema.dump(comment),
        }, 200

    def delete(self, cache_comment_id):
        # find comment
        comment = CacheComment.query.filter_by(
            id_=cache_comment_id, deleted=False
        ).first_or_404()

        # ensure current_user is authorized
        if current_user != comment.author and current_user.role != User.Role.Admin:
            return 403

        # mark comment as deleted
        comment.deleted = True
        db.session.commit()

        return {"msg": "cache comment deleted"}, 200
