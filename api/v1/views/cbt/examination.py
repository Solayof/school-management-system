"""examination endpoints
"""
from datetime import date
from flasgger import swag_from
from flask import abort, jsonify, request
from sqlalchemy.orm.attributes import flag_modified
from api.v1.views.admin import admin as admbp
from models.customExcept import InvalidAdmin
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


def was_published(obj):
      return obj.was_published()


@admbp.route("/examinations/", methods=["GET"], strict_slashes=False)
@swag_from('', methods=['GET'])
def getExamination():
    """get all examinations in database

    Returns:
        json: response
    """ 
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
    paginate = Examination.paginate(page=page, per_page=per_page)
    _, exams, next_page = paginate
    new_exams = list(filter(was_published, exams.all()))
    results = {
        "page": page,
        "total": len(new_exams),
        "per_page": per_page,
        "next_page": next_page,
        "exams": [exam.to_dict() for exam in new_exams]
    }
    return jsonify(results), 200


@admbp.route("/examinations/<exam_id>", methods=["GET"], strict_slashes=False)
@swag_from('', methods=['GET'])
def getOneExamination(exam_id):
    # get examination by id
    exam = Examination.query.filter_by(id=exam_id).one_or_none()
    if exam is None or exam.was_published() is False:
        # if examination does not exist or not published
        abort(404)
    return jsonify(exam.to_dict())


@admbp.route("/examinations/<exam_id>/items", methods=["GET"], strict_slashes=False)
@swag_from('', methods=['GET'])
def getExaminationItems(exam_id):
    # get examination by id
    exam = Examination.query.filter_by(id=exam_id).one_or_none()
    if exam is None or exam.was_published() is False:
        # if examination does not exist or not published
        abort(404)
    
    items = exam.items
    results = {
        "total": len(items),
        "items": [item.to_dict() for item in items]
    }
    return jsonify(results), 200
