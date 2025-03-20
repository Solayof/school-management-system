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


@portal.route("/parents/<parent_id>", methods=["GET"], strict_slashes=False)
@swag_from('../documentations/portal/parent/parent_id.yml', methods=['GET'])
def parent(parent_id=None):
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
    if request.method == "GET":
        # To retrieve parent
        return jsonify(parent.to_dict()), 200

@portal.route("/parents", methods=["GET"])
@swag_from('../documentations/portal/parent/parents.yml', methods=['GET'])
def parents():
    """parent route
        GET: get all parents default limit of 10 parent
        POST: create new parent
    """
    if request.method == "GET":
        try:
            page = abs(int( request.args.get("page", 1)))
        except ValueError:
            abort(400)
        try:
            per_page = abs(int(request.args.get("per_page", 10)))
        except ValueError:
            abort(400)
        if page <= 0 or per_page <= 0:
            return abort(400)
        paginate = Parent.paginate(page=page, per_page=per_page)
        count, parents, next_page = paginate
        results = {
            "page": page,
            "total": count,
            "per_page": per_page,
            "next_page": next_page,
            "results": [parent.to_dict() for parent in parents.all()]
        }
        return jsonify(results), 200

@portal.route("/parents/<parent_id>/children", methods=["GET"], strict_slashes=False)
def children(parent_id=None):
    """retrieve parent wth given id i.e parent_id
    

    Args:
        parent_id (str): id of parent to retrieve or
    """
    if parent_id == "me":
                parent_id = request.current_user.id
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
    if request.method == "GET":
        try:
            page = abs(int( request.args.get("page", 1)))
        except ValueError:
            return jsonify({"page": "page number not an intiger"}), 422
        try:
            perpg = abs(int(request.args.get("per_page", 10)))
        except ValueError:
            return jsonify({"per_page": "number per page not an intiger"}), 422
        
        if perpg == 0  or page == 0:
            abort(400)
        offset = (page - 1) * perpg
        length = len(parent.children)
        if offset >= length:
            abort(404)
        remain = length - offset
        end = offset + perpg if remain >= perpg else offset + remain

        children = [
            {
                "page": page,
                "total": len(parent.children),
                "next_page": page + 1 if page * perpg < len(parent.children) else 1
            },

            [
            parent.children[i].to_dict()
             for i in  range(offset, end)]
        ]
        return jsonify(children), 200
