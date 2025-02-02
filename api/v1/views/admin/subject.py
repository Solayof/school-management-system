"""subject endpoints
"""
from datetime import date
from flasgger import swag_from
from flask import abort, jsonify, request
from sqlalchemy.orm.attributes import flag_modified
from api.v1.views.admin import admin as admbp
from models.customExcept import InvalidAdmin
from models.cbt.examination import Examination
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

@admbp.route("/subjects/", methods=["GET", "POST"], strict_slashes=False)
def subjects():
    """Retrrieve subjects or create subject

    Returns:
        json: json response
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
        paginate = Subject.paginate(page=page, per_page=per_page)
        count, subjects, next_page = paginate
        results = {
            "page": page,
            "total": count,
            "per_page": per_page,
            "next_page": next_page,
            "results": [subject.to_dict() for subject in subjects.all()]
        }
        return jsonify(results), 200

# POST method
    # Only teacher who is an admin with creat privilege can POST.
    # The teacher must have admin privileges
    admin = request.admin
    if admin.privileges is None:
        abort(401)
    if admin.privileges.get("create") is False:
        abort(401)
    info = request.get_json(silent=True)
    if info is None:
        abort(400, "Not a JSON")
    
    if not info.get("name"):
        abort(400, "Missing name")
    name = info.get("name")
    query = Subject.query.filter_by(name=name).one_or_none()
    if query:
        msg = {"Error": f"subject of with name: {name} exist"}
        return jsonify(msg), 403
    if not info.get("code"):
        abort(400, "Missing code")
    code = info.get("code")
    query = Subject.query.filter_by(code=code).one_or_none()
    if query:
        msg = {"Error": f"subject of with name: {code} exist"}
        return jsonify(msg), 403
    subject = Subject()
    for k, v in info.items():
        if k != "id" and hasattr(Subject, k):
            setattr(subject, k, v)
    subject.save()
    return jsonify(subject.to_dict()), 201

@admbp.route("/subjects/<subject_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def subject(subject_id):
    """Retrieve, update or delete specific subject

    Args:
        subject_id (str): subject id or code to retrieve, update or delete
    """    
    # ge subject by id
    subject = Subject.query.filter_by(id=subject_id).one_or_none()
    if not subject:
        # get subject by code
        subject = Subject.query.filter_by(code=subject_id).one_or_none()
        if subject is None:
            # if subject does not exist
            abort(404)
 # GET method
    if request.method == "GET":
        return jsonify(subject)
    
     # Only teacher who is an admin can DELETE and PUT.
    # The teacher must have admin privileges
    admin = request.admin
    if admin.privileges is None:
        abort(401)

# DELETE method
    if request.method == "DELETE":
        if admin.privileges.get("delete") is False:
            abort(401)
        subject.delete()
        return jsonify({}), 204
 
 # PUT method   
    if admin.privileges.get("update") is False:
        abort(401)
    
    info = request.get_json(silent=True)
    if info is None:
        abort(400, "Not a JSON")
    if info.get("name"):
        name = info.get("name")
        query = Subject.query.filter_by(name=name)
        if query.where(Subject.id!=subject.id).one_or_none():
            msg = {"Error": f"subject of with name: {name} exist"}
            return jsonify(msg), 403
    if info.get("code"):
        code = info.get("code")
        query = Subject.query.filter_by(code=code)
        if query.where(Subject.id!=subject.id).one_or_none():
            msg = {"Error": f"subject of with name: {code} exist"}
            return jsonify(msg), 403
    for k, v in info.items():
        if k not in ["created_at", "id"] and hasattr(Subject, k):    
            setattr(subject, k, v)
    subject.save()
    return jsonify(subject.to_dict()), 202

@admbp.route("/subjects/<subject_id>/courses", methods=["GET"], strict_slashes=False)
def subject_courses(subject_id):
    """Retrieve courses or assign course to the subject or create course.

    Args:
        subject_id (str): id or code of the subject to retrieve its courses, assign course or create course

    Returns:
        json: json response
    """    
    # ge subject by id
    subject = Subject.query.filter_by(id=subject_id).one_or_none()
    if not subject:
        # get subject by code
        subject = Subject.query.filter_by(code=subject_id).one_or_none()
        if subject is None:
            # if subject does not exist
            abort(404)

    try:
        page = abs(int( request.args.get("page", 1)))
    except ValueError:
        abort(400)
    try:
        perpg = abs(int(request.args.get("per_page", 10)))
    except ValueError:
        abort(400)
    if perpg == 0  or page == 0:
        abort(400)
    offset = (page - 1) * perpg
    length = len(subject.courses)
    if offset >= length:
        abort(400)
    remain = length - offset
    end = offset + perpg if remain >= perpg else offset + remain
    children = [{
        
            "page": page,
            "total": len(subject.courses),
            "next_page": page + 1 if page * perpg < len(subject.courses) else 1
    },

        [
        subject.courses[i].to_dict()
            for i in  range(offset, end)]
    ]
    return jsonify(children), 200
