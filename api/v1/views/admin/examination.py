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


@admbp.route("/examinations/", methods=["POST"], strict_slashes=False)
@swag_from('', methods=['POST'])
def postExamination():
    # Get the request data
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


@admbp.route("/examinations/<exam_id>", methods=["PUT", "DELETE"], strict_slashes=False)
@swag_from('', methods=['POST'])
def updateExamination(exam_id):
    # Get the exam with provided id
    exam = Examination.query.filter_by(id=exam_id).one_or_none()
    # Check if the exam exist
    if not exam:
        # No exam with such id provided
        abort(404)

# DELETE Method
    if request.method == "DELETE":
        exam.delete()
        return jsonify({}), 204
    
# PUT Method
    # Get the request data
    info = request.get_json(silent=True)
    if info is None:
        abort(400, "Not a JSON")

    for k, v in info.items():
        if hasattr(Examination, k):
            if k == "pub_date":
                try:
                    v = date.fromisoformat(v)
                except ValueError:
                    continue
            setattr(exam, k, v)
    exam.save()
    return jsonify(exam.to_dict()), 202
