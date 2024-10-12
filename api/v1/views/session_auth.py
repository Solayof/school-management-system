#usr/bin/python3
from os import getenv
# from api.v1.app import app
from api.v1.views.portal import portal
from flask import abort, jsonify, request
from models.portal.user import User


@portal.route("/auth_session/logout", methods=["DELETE"], strict_slashes=False)
def session_logout():
    """login out session
    """
    from api.v1.auth.session_db_auth import SessionDbAuth
    auth = SessionDbAuth()
    logout = auth.destry_sesion(request)
    if not logout:
        abort(404)
    return jsonify({})


@portal.route("/auth_session/login", methods=["POST"], strict_slashes=False)
#@app.route("/api/v1/auth_session/login", methods=["POST"], strict_slashes=False)
def sesstion_login():
    """login session
    """
    email = request.form.get("email")
    password = request.form.get("password")
    user = User.query.filter(User.email==email).one_or_none()
    if user is None:
        return jsonify({"email": "Invalid or missing email"})
    if not password:
        return jsonify({"password": "missing password"})
    if not user.is_valid_password(password):
        return jsonify({"password": "Invalid password"})
    from api.v1.auth.session_db_auth import SessionDbAuth
    auth = SessionDbAuth()
    session_id = auth.create_session(user.id)
    session_cookie = getenv("SESSION_NAME")
    res = jsonify(user.to_dict())
    res.set_cookie(session_cookie, session_id)
    return res    
