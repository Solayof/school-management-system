"""parent endpoints
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


@admbp.route("parent/<parent_id>", methods=["GET"])
def parents(parent_id):
    """retrieve parent wth given id i.e parent_id
    

    Args:
        parent_id (str): id of parent to retrieve or
    """
    parent = Parent.get(parent_id)
    if not parent:
    # if parent does not exist
        abort(404)

    # To retrieve parent
    return jsonify(parent.to_dict())
