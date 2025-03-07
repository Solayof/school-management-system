
from flask import request
from os import getenv


class Auth:
    def require_auth(self, path, excluded_paths):
        if path is None or excluded_paths is None:
            return True
        for i in excluded_paths:
            if i.endswith("*") and path.startswith(i[:-1]):
                return False
            elif i in {path, path + "/"}:
                return False
        return True
    
    def authentication_header(self, request=None):
        if request is None  or "Authentication" not in request.headers:
            return None
        return request.headers.get("Authentication")
    
    def current_user(self, request=None):
        return None
    
    def session_cookie(self, request=None):
        if request is None:
            return None
        return request.cookies.get(getenv("SESSION_NAME"))
