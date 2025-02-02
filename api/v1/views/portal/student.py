"""student route
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


@portal.route("/students", methods=["GET", "POST"])
@swag_from('../documentations/portal/student/students.yml', methods=['GET', 'POST'])
def students():
    """student route
        GET: get all students default limit of 10 student
        POST: create new student
    """
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
    paginate = Student.paginate(page=page, per_page=per_page)
    count, students, next_page = paginate
    results = {
        "page": page,
        "total": count,
        "per_page": per_page,
        "next_page": next_page,
        "results": [student.to_dict() for student in students.all()]
    }
    return jsonify(results), 200

    
@portal.route("/students/<student_id>", methods=["GET"], strict_slashes=False)
@swag_from('../documentations/portal/student/student_id.yml', methods=['GET'])
def student(student_id=None):
    """retrieve student wth given id i.e student_id
    

    Args:
        student_id (str): id of student to retrieve or
    """
    if student_id == "me":
                student_id = request.current_user.id
    # ge student by id
    student = Student.query.filter_by(id=student_id).one_or_none()
    if not student:
        # get student by username
        student = Student.query.filter_by(username=student_id).one_or_none()
        if student is None:
            # Get student by email
            student = Student.query.filter_by(email=student_id).one_or_none()
            if student is None:
                # if student does not exist
                abort(404)
 
 # GET method       
    return jsonify(student.to_dict()), 200
