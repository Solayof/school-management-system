"""parent endpoints
"""
from datetime import date
from flasgger import swag_from
from flask import abort, jsonify, request
from api.v1.views.portal import portal
from models.cbt.examination import Examination
from models.cbt.option import Option
from models.cbt.question import Question
from models.cbt.response import Response
from models.cbt.score import Score
from models.portal.admin import Admin
from models.portal.admission import Admission
from models.portal.Class import Class
from models.portal.course import Course
from models.portal.department import Department
from models.portal.parent import Parent
from models.portal.student import Student
from models.portal.subject import Subject
from models.portal.teacher import Teacher
from models.portal.user import User


@portal.route("/parents/<parent_id>", methods=["PUT", "DELETE"], strict_slashes=False)
@swag_from('../documentations/portal/parent/parent_id.yml', methods=['PUT', 'DELETE'])
def adparent(parent_id=None):
    """retrieve parent wth given id i.e parent_id
    

    Args:
        parent_id (str): id of parent to retrieve or
    """
    # ge parent by id
    parent = Parent.query.filter_by(id=parent_id).one_or_none()
    if not parent:
        # get parent by username
        parent = Parent.query.filter_by(username=parent_id).one_or_none()
        if parent is None:
            # Get parent by email
            parent = Parent.query.filter_by(email=parent_id).one_or_none()
            if parent is None:
                 # if parent does not exist
                abort(404)
    admin = request.admin
# DELETE method
    if request.method == "DELETE":
        if admin.privileges.get("delete") is False:
            abort(401)
        parent.delete()
        return jsonify({}), 204
    
    if admin.privileges.get("update") is False:
        abort(401)
    
    
    # PUT method
    if admin.privileges.get("update") is False:
            abort(401)
    info = request.get_json(silent=True)
    if info is None:
        abort(400, "Not a JSON")
    for k, v in info.items():
        if k not in ["created_at", "id"] and hasattr(Parent, k):
            if k == "dob":
                try:
                    v = date.fromisoformat(v)
                except ValueError:
                    return jsonify({"Error": f"wrong {k} date format"}), 400
            if k =="username":
                if User.query.filter_by(username=v).one_or_none():
                    return jsonify({"Error": f"User with {v} exist"}), 400
            if k =="email":
                if User.query.filter_by(email=v).one_or_none():
                    return jsonify({"Error": f"User with {v} exist"}), 400
            setattr(parent, k, v)
    parent.save()
    return jsonify(parent.to_dict()), 202
        

@portal.route("/parents", methods=["POST"])
@swag_from('../documentations/portal/parent/parents.yml', methods=['POST'])
def adparents():
    """parent route
        GET: get all parents default limit of 10 parent
        POST: create new parent
    """
    admin = request.admin
    if admin.privileges.get("create") is False:
        abort(401)
    info = request.get_json(silent=True)
    if info is None:
        abort(400, "Not a JSON")
    
    if not info.get("username"):
        abort(400, "Missing username")
    if User.query.filter_by(username=info.get("username")).one_or_none():
        abort(400, f"User with username {info.get('username')} exist")
    if not info.get("email"):
        abort(400, "Missing email")
    if User.query.filter_by(username=info.get("email")).one_or_none():
        abort(400, f"User with email {info.get('email')} exist")
    parent = Parent()
    for k, v in info.items():
        if k != "id" and hasattr(Parent, k):
            if k == "dob":
                try:
                    v = date.fromisoformat(v)
                except ValueError:
                    continue
            setattr(parent, k, v)
    parent.save()
    return jsonify(parent.to_dict()), 201