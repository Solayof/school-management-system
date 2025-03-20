#usr/bin/python3
from os import getenv
# from api.v1.app import app
from api.v1.views.portal import portal
from flask import abort, jsonify, request
from models.portal.parent import Parent
from models.portal.student import Student
from models.portal.teacher import Teacher
from models.portal.user import User


@portal.route("/auth_session/logout", methods=["DELETE"], strict_slashes=False)
def session_logout():
    """login out session
    """
    from api.v1.auth.session_db_auth import SessionDbAuth
    auth = SessionDbAuth()
    logout = auth.destory_sesion(request)
    if not logout:
        abort(404)
    return jsonify({})


@portal.route("/auth_session/login", methods=["POST"], strict_slashes=False)
# @app.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def sesstion_login():
    """login session
    """
    email = request.form.get("email")
    print(email)
    password = request.form.get("password")
    user = User.query.filter(User.email==email).one_or_none()
    if user is None:
        username = request.form.get("username")
        user = User.query.filter(User.username==username).one_or_none()
        if user is None:
            return jsonify({"id": "Invalid username or email"}), 400
    if not password:
        return jsonify({"password": "missing password"}), 400
    if not user.is_valid_password(password):
        return jsonify({"password": "Invalid password"}), 400
    from api.v1.auth.session_db_auth import SessionDbAuth
    auth = SessionDbAuth()
    session_id = auth.create_session(user.id)
    session_cookie = getenv("SESSION_NAME")
    student = Student.get(user.id)
    teacher = Teacher.get(user.id)
    if student:
        res = jsonify(student.to_dict())
    elif teacher:
        res = jsonify(teacher.to_dict())
    else:
        res = jsonify(Parent.get(user.id).to_dict())
    res.set_cookie(session_cookie, session_id, path='/', secure=True, httponly=True, samesite='None')
    return res, 201 


@portal.route("/auth_session", methods=["GET"], strict_slashes=False)
# @app.route("/auth_session", methods=["GET"], strict_slashes=False)
def sesstion_user():
    """login session
    """
    return jsonify(request.current_user.to_dict())