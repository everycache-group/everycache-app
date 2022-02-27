from flask import Blueprint, abort, current_app, jsonify, request
from flask_jwt_extended import current_user, get_jwt, jwt_required

from everycache_api.auth.helpers import (
    create_user_access_token,
    create_user_refresh_token,
    is_token_revoked,
    revoke_all_user_tokens,
    revoke_token,
    save_encoded_token,
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
        401:
          description: incorrect credentials
      security: []
    """
    if not request.is_json:
        abort(400, "Missing JSON payload in request.")

    email = request.json.get("email", None)
    password = request.json.get("password", None)

    errors = {}

    if email is None:
        errors["email"] = ["Missing data for required field."]

    if password is None:
        errors["password"] = ["Missing data for required field."]

    if errors:
        return jsonify(errors=errors), 400

    user = User.query.filter_by(email=email).first()
    if user is None or not user.verify_password(password):
        abort(401, "Incorrect email and password combination.")

    if user.deleted:
        abort(401, "Account deleted.")

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
        abort(401, "Invalid or expired token.")

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
                    example: Access token revoked.
        400:
          description: bad request
        401:
          description: unauthorized
    """
    revoke_token(get_jwt())

    return {"message": "Access token revoked."}, 200


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
                    example: Refresh token revoked.
        400:
          description: bad request
        401:
          description: unauthorized
    """
    revoke_token(get_jwt())

    return {"message": "Refresh token revoked."}, 200


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
                    example: All user tokens revoked.
        400:
          description: bad request
        401:
          description: unauthorized
    """
    revoke_all_user_tokens(current_user)

    return {"message": "All user tokens revoked."}, 200


@blueprint.errorhandler(400)
def handle_400_error(e):
    return {"message": e.description}, 400


@blueprint.errorhandler(401)
def handle_401_error(e):
    return {"message": e.description}, 401


@jwt.user_lookup_loader
def user_loader_callback(jwt_headers, jwt_payload):
    user_id = jwt_payload["sub"]
    user = User.query_ext_id(user_id, False).first()

    if not user:
        # token is valid but user is no longer in database; return generic reason
        abort(401, "Invalid or expired token.")

    if user.deleted:
        # user is deleted and this token should have been revoked; revoke all tokens
        revoke_all_user_tokens(user)
        abort(401, "Token has been revoked.")

    return user


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_headers, jwt_payload):
    if is_token_revoked(jwt_payload):
        abort(401, "Token has been revoked.")

    return False


@jwt.expired_token_loader
def expired_token_callback(jwt_headers, jwt_payload):
    abort(401, "Token has expired.")


@blueprint.before_app_first_request
def register_views():
    apispec.spec.path(view=login, app=current_app)
    apispec.spec.path(view=refresh, app=current_app)
    apispec.spec.path(view=revoke_access_token, app=current_app)
    apispec.spec.path(view=revoke_refresh_token, app=current_app)
    apispec.spec.path(view=revoke_all_tokens, app=current_app)
