"""class endpoints
"""
from datetime import date, datetime
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


@admbp.route("/classes/", methods=["GET", "POST"], strict_slashes=False)
@swag_from('../documentations/portal/Class/classes.yml', methods=['GET', 'POST'])
def classes():
    """get all classes or create a class

    Returns:
        json: response
    """    
    if request.method == "GET":
        try:
            page = abs(int( request.args.get("page", 1)))
        except ValueError:
            return abort(400)
        try:
            per_page = abs(int(request.args.get("per_page", 1)))
        except ValueError:
            return abort(400)

        if page <= 0 or per_page <= 0:
            return abort(400)
        paginate = Class.paginate(page=page, per_page=per_page)
        count, classes, next_page = paginate
        results = {
            "page": page,
            "total": count,
            "per_page": per_page,
            "next_page": next_page,
            "results": [clas.to_dict() for clas in classes.all()]
        }
        return jsonify(results), 200

# POST method
    # Only teacher who is an admin with creat privilege can POST.
    # The teacher must have admin privileges
    admin = request.admin
    if admin.privileges is None:
        abort(401)
    if admin.privileges.get("create") is False:
        return jsonify({"PERMISSION":"CREATE PERMISSION DENIED"}), 401
    info = request.get_json(silent=True)
    if info is None:
        abort(400, "Not a JSON")
    
    if not info.get("className"):
        abort(400, "Missing class name")
    
    className = info.get("className").upper()
    code = className.replace(" ", "-")
    yr = datetime.now().strftime("%y")
    code = code + "-" + f"20{yr}-20{int(yr) + 1}"
    clas = Class.query.filter_by(code=code).one_or_none()
    
    if clas is not None:
        return jsonify(clas.to_dict()), 200

    clas = Class(className=info.get("className"))

    clas.save()
    return jsonify(clas.to_dict()), 201

@admbp.route("/classes/<clas_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
@swag_from('../documentations/portal/Class/class_id.yml', methods=['GET', 'PUT', 'DELETE'])
def clas(clas_id):
    """get, update and delete specific class

    Args:
        clas_id (str): id od code of the class to get update or delete
    """    
    # ge class by id
    clas = Class.query.filter_by(id=clas_id).one_or_none()
    if not clas:
        # get class by code
        clas = Class.query.filter_by(code=clas_id).one_or_none()
    if clas is None:
        # if class does not exist
        abort(404)
 # GET method
    if request.method == "GET":
        return jsonify(clas.to_dict())
    
     # Only teacher who is an admin can DELETE and PUT.
    # The teacher must have admin privileges
    admin = request.admin
    if admin.privileges is None:
        abort(401)

# DELETE method
    if request.method == "DELETE":
        if admin.privileges.get("delete") is False:
            abort(401)
        clas.delete()
        return jsonify({}), 204
 
 # PUT method   
    if admin.privileges.get("update") is False:
        abort(401)
    
    info = request.get_json(silent=True)
    if info is None:
        abort(400, "Not a JSON")

    if info.get("code"):
        code = info.get("code")
        query = Class.query.filter_by(code=code)
        if query.where(Class.id!=clas.id).one_or_none():
            msg = {"Error": f"class of with name: {code} exist"}
            return jsonify(msg), 403
    for k, v in info.items():
        if k not in ["created_at", "id"] and hasattr(Class, k):    
            setattr(clas, k, v)
    clas.save()
    return jsonify(clas.to_dict()), 201

@admbp.route("/classes/<clas_id>/courses", methods=["GET"], strict_slashes=False)
def class_courses(clas_id):
    """get and update a specific class course

    Args:
        clas_id (str): id or code of the class to get or update its course
    """    
    # ge clas by id
    clas = Class.query.filter_by(id=clas_id).one_or_none()
    if not clas:
        # get clas by code
        clas = Class.query.filter_by(code=clas_id).one_or_none()
        if clas is None:
            # if clas does not exist
            abort(404)
    
    
    try:
        page = abs(int( request.args.get("page", 1)))
    except ValueError:
        abort(400)
    try:
        perpg = abs(int(request.args.get("per_page", 10)))
    except ValueError:
        abort(400)

    if perpg <= 0  or page <= 0:
        abort(400)
    offset = (page - 1) * perpg
    length = len(clas.courses)
    if offset >= length and length != 0:
        abort(404)
    remain = length - offset
    end = offset + perpg if remain >= perpg else offset + remain

    courses = [{
        
            "page": page,
            "total": len(clas.courses),
            "next_page": page + 1 if page * perpg < len(clas.courses) else 1
    },

        [
        clas.courses[i].to_dict()
            for i in  range(offset, end)]
    ]
    return jsonify(courses), 200


@admbp.route("/classes/<clas_id>/formteacher", methods=["GET"], strict_slashes=False)
def class_form_teacher(clas_id):
    """Retrieve, and upadte specific class form teachers

    Args:
        clas_id (str): the id of the class to retreive or update its form teachers

    Returns:
        json: json response
    """ 
    # ge clas by id
    clas = Class.query.filter_by(id=clas_id).one_or_none()
    if not clas:
        # get clas by code
        clas = Class.query.filter_by(code=clas_id).one_or_none()
        if clas is None:
            # if clas does not exist
            abort(404)

    try:
        page = abs(int( request.args.get("page", 1)))
    except ValueError:
        abort(400)
    try:
        perpg = abs(int(request.args.get("per_page", 10)))
    except ValueError:
        abort(400)
    
    if perpg <= 0  or page <= 0:
        abort(400)
    offset = (page - 1) * perpg
    length = len(clas.form_teacher)
    if offset >= length and length != 0:
        abort(404)
    remain = length - offset
    end = offset + perpg if remain >= perpg else offset + remain

    form_teacher = [{
        
            "page": page,
            "total": len(clas.form_teacher),
            "next_page": page + 1 if page * perpg < len(clas.form_teacher) else 1
    },

        [
        clas.form_teacher[i].to_dict()
            for i in  range(offset, end)]
    ]
    return jsonify(form_teacher), 200


@admbp.route("/classes/<clas_id>/students", methods=["GET"], strict_slashes=False)
def class_students(clas_id):
    """Retrieve, and upadte specific class form students

    Args:
        clas_id (str): the id of the class to retreive or update its students

    Returns:
        json: json response
    """ 
    # ge clas by id
    clas = Class.query.filter_by(id=clas_id).one_or_none()
    if not clas:
        # get clas by code
        clas = Class.query.filter_by(code=clas_id).one_or_none()
        if clas is None:
            # if clas does not exist
            abort(404)
    

    try:
        page = abs(int( request.args.get("page", 1)))
    except ValueError:
        return jsonify({"page": "page number not an intiger"}), 422
    try:
        perpg = abs(int(request.args.get("per_page", 10)))
    except ValueError:
        return jsonify({"per_page": "number per page not an intiger"}), 422
    
    if perpg <= 0  or page <= 0:
        abort(400)
    offset = (page - 1) * perpg
    length = len(clas.students)
    if offset >= length and length != 0:
        abort(404)
    remain = length - offset
    end = offset + perpg if remain >= perpg else offset + remain
    students =[ {
        
            "page": page,
            "total": len(clas.students),
            "next_page": page + 1 if page * perpg < len(clas.students) else 1
    },

        [
        clas.students[i].to_dict()
            for i in  range(offset, end)]
    ]
    return jsonify(students), 200


@admbp.route("/classes/<clas_id>/examinations", methods=["GET"], strict_slashes=False)
def class_examinations(clas_id):
    """Retrieve, and upadte specific class examinations

    Args:
        clas_id (str): the id of the class to retreive or update its examinations

    Returns:
        json: json response
    """ 
    # ge clas by id
    clas = Class.query.filter_by(id=clas_id).one_or_none()
    if not clas:
        # get clas by code
        clas = Class.query.filter_by(code=clas_id).one_or_none()
        if clas is None:
            # if clas does not exist
            abort(404)

    try:
        page = abs(int( request.args.get("page", 1)))
    except ValueError:
        abort(400) 
    try:
        perpg = abs(int(request.args.get("per_page", 10)))
    except ValueError:
        abort(400)
    
    if perpg <= 0  or page <= 0:
        abort(400)
    offset = (page - 1) * perpg
    length = len(clas.examinations)
    if offset >= length and length != 0:
        abort(404)
    remain = length - offset
    end = offset + perpg if remain >= perpg else offset + remain
    examinations = [{
        
            "page": page,
            "total": len(clas.examinations),
            "next_page": page + 1 if page * perpg < len(clas.examinations) else 1
    },

        [
        clas.examinations[i].to_dict()
            for i in  range(offset, end)]
    ]
    return jsonify(examinations), 200
