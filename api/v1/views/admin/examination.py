"""examination endpoints
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


@admbp.route("/examinations/", methods=["POST", "GET"], strict_slashes=False)
@swag_from('', methods=['POST'])
def postExamination():
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
    # Grt method
    if request.method == "GET":
        paginate = Examination.paginate(page=page, per_page=per_page)
        count, exams, next_page = paginate
        results = {
            "page": page,
            "total": count,
            "per_page": per_page,
            "next_page": next_page,
            "exams": [exam.to_dict() for exam in exams.all()]
        }
        return jsonify(results), 200


    admin = request.admin
    if admin.privileges is None:
        abort(401)
    
# POST Method
    # Get the request data
    if admin.privileges.get("create") is False:
        abort(401)
    info = request.get_json(silent=True)
    if info is None:
        abort(400, "Not a JSON")

    if not info.get("name"):
        abort(400, "Missing name")
    if not info.get("mode"):
        abort(400, "Missing mode")
    if not info.get("term"):
        abort(400, "Missing term")
    exam = Examination()
    for k, v in info.items():
        if hasattr(Examination, k):
            if k == "pub_date":
                try:
                    v = date.fromisoformat(v)
                except ValueError:
                    continue
            setattr(exam, k, v)
    exam.save()
    return jsonify(exam.to_dict()), 201


@admbp.route("/examinations/<exam_id>", methods=["PUT", "DELETE", "GET"], strict_slashes=False)
@swag_from('', methods=['POST'])
def updateExamination(exam_id):
    # Get the exam with provided id
    exam = Examination.query.filter_by(id=exam_id).one_or_none()
    # Check if the exam exist
    if not exam:
        # No exam with such id provided
        abort(404)
# GET method
    if request.method == "GET":
         return jsonify(exam.to_dict())

    admin = request.admin
    if admin.privileges is None:
        abort(401)
# DELETE Method
    if request.method == "DELETE":
        if admin.privileges.get("delete") is False:
            abort(401)
        exam.delete()
        return jsonify({}), 204
    
# PUT Method
    if admin.privileges.get("update") is False:
        abort(401)
    # Get the request data
    info = request.get_json(silent=True)
    if info is None:
        abort(400, "Not a JSON")

    for k, v in info.items():
        if k == "id":
             continue
        if hasattr(Examination, k):
            if k == "pub_date":
                try:
                    v = date.fromisoformat(v)
                except ValueError:
                    continue
            setattr(exam, k, v)
    exam.save()
    return jsonify(exam.to_dict()), 202

@admbp.route("/examinations/session/<session>", methods=["GET"], strict_slashes=False)
@swag_from('', methods=['GET'])
def getExaminationBySession(session):
    # get examination by id
    exams = Examination.query.filter_by(session=session).all()
    if len(exams) == 0:
          abort(404)
    try:
            page = abs(int( request.args.get("page", 1)))
    except ValueError:
            return abort(400)
    try:
            perpg = abs(int(request.args.get("per_page", 1)))
    except ValueError:
            return abort(400)

    if perpg == 0  or page == 0:
            abort(400)
    offset = (page - 1) * perpg
    
    length = len(exams)
    if offset >= length:
        abort(400)
    remain = length - offset
    end = offset + perpg if remain >= perpg else offset + remain
    results = {
        "page": page,
        "total": length,
        "per_page": perpg,
        "next_page":  page + 1 if page * perpg < length else 1,
         "exams": [exam.to_dict() for  exam in exams[offset:end]]
    }
    return jsonify(results), 200
