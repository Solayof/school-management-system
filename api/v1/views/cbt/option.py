"""option endpoints
"""
from datetime import date
from flasgger import swag_from
from flask import abort, jsonify, request
from sqlalchemy.orm.attributes import flag_modified
from api.v1.views.cbt import cbt
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


@cbt.route("/options/<option_id>", methods=["GET"], strict_slashes=False)
@swag_from('', methods=['GET'])
def getOneCBToption(option_id):
# Get exam by id
    option = Option.get(option_id)
    if option is None or option.question is None:
        abort(404)
    if option.question.was_published() is False:
        abort(404)
    option_dict = option.to_dict()
    option_dict.pop('answer', None)
    option_dict.pop('note', None)
    print(option_dict)
     
    return jsonify(option_dict), 200