"""teacher endpoints
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
from models.portal.parent import Parent
from models.portal.student import Student
from models.portal.subject import Subject
from models.portal.teacher import Teacher
from models.portal.user import User


@admbp.route("/", methods=["GET", "POST"], strict_slashes=False)
def get_admin():
    """Retrieve and create admin user
    """ 
    userId = request.current_user.id
    admUser = Admin.query.filter(Admin.teacher_id==userId).one_or_none()
    if admUser is None:
        abort(401)
    if admUser.privileges is None:
        abort(401)
    

# GET Method
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
        paginate = Admin.paginate(page=page, per_page=per_page)
        count, admins, next_page = paginate
        results = {
            "page": page,
            "total": count,
            "per_page": per_page,
            "next_page": next_page,
            "results": [adm.to_dict() for adm in admins.all()]
        }
        return jsonify(results), 200

# POST Method
    if admUser.privileges.get("superuser") is False:
        abort(401)
    info = request.get_json(silent=True)
    if info is None:
        abort(400, "Not a JSON")
    
    teacher_id = info.get("teacherId")
    if teacher_id is None:
        abort(400, "Missing teacher id")
    teacher = Teacher.query.filter_by(_id=teacher_id).one_or_none()
    if teacher is None:
        abort(400, f"No teacher with {teacher_id} as id")
    if teacher.isAdmin() is False:
       adm = Admin(teacher_id=teacher_id)
       try:
           adm.save()
           return jsonify(adm.to_dict())
       except InvalidAdmin as error:
           return jsonify(error)

    adm = Admin.query.filter(Admin.teacher_id==teacher_id).one()
    return jsonify(adm.to_dict()), 200
    


@admbp.route("/<admin_id>", methods=["GET", "PUT"], strict_slashes=False)
def update_admin(admin_id=None):
    """Retrieve a specific user and update specific user privileges

    Args:
        admin_id (str, optional): id of the specific user. Defaults to None.
    """
    userId = request.current_user.id
    admUser = Admin.query.filter(Admin.teacher_id==userId).one_or_none()
    if admUser is None:
        abort(401)
    if admUser.privileges is None:
        abort(401)
     
    admin = Admin.get(admin_id)
    if admin is None:
        abort(404)

# GET method
    if request.method == "GET":
        return jsonify(admin.to_dict()), 200

# PUT method
    if admUser.privileges.get("superuser") is False:
        abort(401)
    info = request.get_json(silent=True)
    if info is None:
        abort(400, "Not a JSON")
    authKey = ["update", "create", "superadmin", "delete"]

    for k, v in info.items():
        if v.lower() == "false":
            v = False
        elif v.lower() == "true":
            v = True
        else:       
            return jsonify({"error": "not bool"})
        # Ensure the right kind of privileges are set and 
        # of boolean type
        if k in authKey and isinstance(v, bool):
            admin.privileges[k] = v
    # Ensure SQLAlchemy detect the change in privileges
    flag_modified(admin, "privileges")
    # commit the change to database
    admin.save()
    return jsonify(admin.to_dict()), 202
