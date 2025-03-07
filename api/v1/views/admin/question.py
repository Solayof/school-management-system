"""question endpoints
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


@admbp.route("/questions/<exam_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
# @swag_from('', methods=['GET'])
def oneQuestion(exam_id):
# Get exam by id
    question = Question.get(exam_id)
    # very if question exist or was published
    if question is None:
        # Not Found
        abort(404)
# GET Method
    if request.method == "GET":
        return jsonify(question.to_dict())
    
    admin = request.admin
    if admin.privileges is None:
        abort(401)
# DWLETE Method
    if request.method == "DELETE":
        if admin.privileges.get("delete") is False:
            abort(401)
        question.delete()
        return jsonify({}), 204
# PUT Method
    if admin.privileges.get("update") is False:
        abort(401)
    info = request.get_json(silent=True)
    if info is None:
        abort(400, "Not a JSON")

    for k, v in info.items():
        if k == "id":
            continue
        if hasattr(Question, k):
            if k == "pub_date":
                try:
                    v = date.fromisoformat(v)
                except ValueError:
                    continue
            setattr(question, k, v)
    question.save()
    return jsonify(question.to_dict()), 202


@admbp.route("/questions", methods=["POST"], strict_slashes=False)
# @swag_from('', methods=['POST'])
def createQuestion():
    admin = request.admin
    print("here")
    if admin.privileges is None:
        abort(401)
    if admin.privileges.get("create") is False:
        abort(401)
    # Get the request data
    info = request.get_json(silent=True)
    if info is None:
        abort(400, "Not a JSON")

    if not info.get("content"):
        abort(400, "Missing name")
    if not info.get("mode"):
        abort(400, "Missing mode")

    question = Question()
    for k, v in info.items():
        if hasattr(Question, k):
            if k == "pub_date":
                try:
                    v = date.fromisoformat(v)
                except ValueError:
                    continue
            setattr(question, k, v)
    question.save()
    return jsonify(question.to_dict()), 201