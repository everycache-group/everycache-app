from flask import Blueprint, current_app, request
from flask_jwt_extended import current_user, get_jwt, jwt_required

from everycache_api.auth.helpers import (
    create_user_access_token,
    create_user_refresh_token,
    is_token_revoked,
    load_tokens_from_database_to_storage,
    revoke_all_user_tokens,
    revoke_token,
    save_encoded_token,
)
from everycache_api.extensions import apispec, jwt, redis_client
from everycache_api.models import User

blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@blueprint.route("/login", methods=["POST"])
def login():
    """Authenticate user and return tokens

    ---
    post:
      tags:
        - auth
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                email:
                  type: string
                  example: myuser@example.com
                  required: true
                password:
                  type: string
                  example: P4$$w0rd!
                  required: true
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  access_token:
                    type: string
                    example: myaccesstoken
                  refresh_token:
                    type: string
                    example: myrefreshtoken
        400:
          description: bad request
      security: []
    """
    if not request.is_json:
        return {"msg": "Missing JSON payload in request"}, 400

    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if email is None or password is None:
        return {"msg": "Missing e-mail address or password"}, 400

    user = User.query.filter_by(email=email).first()
    if user is None or not user.verify_password(password):
        return {"msg": "Incorrect email and password combination"}, 400

    access_token = create_user_access_token(user)
    refresh_token = create_user_refresh_token(user)

    save_encoded_token(access_token)
    save_encoded_token(refresh_token)

    return {"access_token": access_token, "refresh_token": refresh_token}, 200


@blueprint.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """Get an access token from a refresh token

    ---
    post:
      tags:
        - auth
      parameters:
        - in: header
          name: Authorization
          required: true
          description: valid refresh token
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  access_token:
                    type: string
                    example: myaccesstoken
        400:
          description: bad request
        401:
          description: unauthorized
    """
    if not current_user:
        return {"msg": "User in refresh token does not exist"}, 401

    access_token = create_user_access_token(current_user)
    save_encoded_token(access_token)

    return {"access_token": access_token}, 200


@blueprint.route("/revoke_access", methods=["DELETE"])
@jwt_required()
def revoke_access_token():
    """Revoke an access token

    ---
    delete:
      tags:
        - auth
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: token revoked
        400:
          description: bad request
        401:
          description: unauthorized
    """
    revoke_token(get_jwt())

    return {"message": "token revoked"}, 200


@blueprint.route("/revoke_refresh", methods=["DELETE"])
@jwt_required(refresh=True)
def revoke_refresh_token():
    """Revoke a refresh token, used mainly for logout

    ---
    delete:
      tags:
        - auth
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: token revoked
        400:
          description: bad request
        401:
          description: unauthorized
    """
    revoke_token(get_jwt())

    return {"message": "token revoked"}, 200


@blueprint.route("/revoke_all", methods=["DELETE"])
@jwt_required()
def revoke_all_tokens():
    """Revoke all tokens, used for logging out of all devices

    ---
    delete:
      tags:
        - auth
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: all tokens revoked
        400:
          description: bad request
        401:
          description: unauthorized
    """
    revoke_all_user_tokens(current_user)

    return {"message": "all tokens revoked"}, 200


@jwt.user_lookup_loader
def user_loader_callback(jwt_headers, jwt_payload):
    user_id = jwt_payload["sub"]

    return User.query_ext_id(user_id).one_or_none()


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_headers, jwt_payload):
    return is_token_revoked(jwt_payload)


@blueprint.before_app_first_request
def register_views():
    apispec.spec.path(view=login, app=current_app)
    apispec.spec.path(view=refresh, app=current_app)
    apispec.spec.path(view=revoke_access_token, app=current_app)
    apispec.spec.path(view=revoke_refresh_token, app=current_app)
    apispec.spec.path(view=revoke_all_tokens, app=current_app)

    if redis_client:
        current_app.logger.info("Loading tokens from database to redis storage...")

        load_tokens_from_database_to_storage()

        current_app.logger.info("Done")
