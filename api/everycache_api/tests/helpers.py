
def get_auth_header(token):
    return {"Authorization": f"Bearer {token}"}


def get_headers_for_user(logged_in_user, logged_in_user_role):
    user, access_token, _ = logged_in_user
    headers = {}
    if logged_in_user_role is not None:
        user.role = logged_in_user_role
        headers = get_auth_header(access_token)
    return headers
