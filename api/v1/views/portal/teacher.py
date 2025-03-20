"""teacher endpoints
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

    
@portal.route("/teachers/<teacher_id>", methods=["GET"], strict_slashes=False)
@swag_from('../documentations/portal/teacher/teacher_id.yml', methods=['GET', 'PUT', 'DELETE'])
def teacher(teacher_id=None):
    """retrieve teacher wth given id, username or email i.e teacher_id
    

    Args:
        teacher_id (str): id, username or email of teacher to retrieve
    """
    if teacher_id == "me":
                teacher_id = request.current_user.id
    # ge teacher by id
    teacher = Teacher.query.filter_by(id=teacher_id).one_or_none()
    if not teacher:
        # get teacher by username
        teacher = Teacher.query.filter_by(username=teacher_id).one_or_none()
        if teacher is None:
            # Get teacher by email
            teacher = Teacher.query.filter_by(email=teacher_id).one_or_none()
            if teacher is None:
                 # if teacher does not exist
                abort(404)
# GET method
    
    return jsonify(teacher.to_dict()), 200
    

@portal.route("/teachers/<teacher_id>/courses", methods=["GET"], strict_slashes=False)
def teacher_courses(teacher_id):
    """Retrieve and update courses of the specified teacher by the unigue identifier

    Args:
        teacher_id (str): the unique identifier of the teacher

    Returns:
        json: json response
    """    
    if teacher_id == "me":
                teacher_id = request.current_user.id
    # ge teacher by id
    teacher = Teacher.query.filter_by(id=teacher_id).one_or_none()
    if not teacher:
        # get teacher by username
        teacher = Teacher.query.filter_by(username=teacher_id).one_or_none()
        if teacher is None:
            # Get teacher by email
            teacher = Teacher.query.filter_by(email=teacher_id).one_or_none()
            if teacher is None:
                 # if teacher does not exist
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
    length = len(teacher.course)
    if offset >= length:
        abort(400)
    remain = length - offset
    end = offset + perpg if remain >= perpg else offset + remain
    courses = {
        
            "page": page,
            "total": len(teacher.courses),
            "next_page": page + 1 if page * perpg < length else 1
        ,

        "courses": [{
        teacher.courses[i].to_dict()
        } for i in  range(offset, end)]
    }
    return jsonify(courses), 200
