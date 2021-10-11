from flask import Blueprint, current_app, request
from flask_jwt_extended import current_user, get_jwt, get_jwt_identity, jwt_required

from everycache_api.auth.helpers import (
    add_token_to_database,
    create_user_access_token,
    create_user_refresh_token,
    is_token_revoked,
    revoke_token,
)
from everycache_api.extensions import apispec, jwt
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
    add_token_to_database(access_token, current_app.config["JWT_IDENTITY_CLAIM"])
    add_token_to_database(refresh_token, current_app.config["JWT_IDENTITY_CLAIM"])

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
    add_token_to_database(access_token, current_app.config["JWT_IDENTITY_CLAIM"])

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
    jti = get_jwt()["jti"]
    user_identity = get_jwt_identity()
    revoke_token(jti, user_identity)
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
    jti = get_jwt()["jti"]
    user_identity = get_jwt_identity()
    revoke_token(jti, user_identity)
    return {"message": "token revoked"}, 200


@jwt.user_lookup_loader
def user_loader_callback(jwt_headers, jwt_payload):
    identity = jwt_payload["sub"]
    return User.query_ext_id(identity).one_or_none()


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_headers, jwt_payload):
    return is_token_revoked(jwt_payload)


@blueprint.before_app_first_request
def register_views():
    apispec.spec.path(view=login, app=current_app)
    apispec.spec.path(view=refresh, app=current_app)
    apispec.spec.path(view=revoke_access_token, app=current_app)
    apispec.spec.path(view=revoke_refresh_token, app=current_app)
