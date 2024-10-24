"""student route
"""
from datetime import date
from flasgger import swag_from
from flask import abort, jsonify, request
from api.v1.views.portal import portal
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


@portal.route("/students", methods=["GET", "POST"])
@swag_from('../documentations/portal/student/students.yml', methods=['GET', 'POST'])
def students():
    """student route
        GET: get all students default limit of 10 student
        POST: create new student
    """
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
    # Only teacher who is an admin with create privilege can POST.
    # The teacher must have admin privileges
    user_id = request.current_user.id
    # Get the teacher instance
    teacher = Teacher.get(user_id)
    if teacher is None:
        #not a teacher, permission denied
        abort(401)
    if teacher.isAdmin() is False:
        abort(401)
    admin = Admin.query.filter(Admin.teacher_id==user_id).one_or_none()
    if admin is None:
        abort(401)
    
    if admin.privileges is None:
        abort(401)
    if admin.privileges.get("create") is False:
        abort(401)
    info = request.get_json(silent=True)
    if info is None:
        abort(400, "Not a JSON")
    
    if not info.get("username"):
        abort(400, "Missing username")
    if User.query.filter_by(username=info.get("username")).one_or_none():
        abort(400, f"User with username {info.get('username')} exist")
    if not info.get("email"):
        abort(400, "Missing email")
    if User.query.filter_by(username=info.get("email")).one_or_none():
        abort(400, f"User with email {info.get('email')} exist")
    if Student.query.filter_by(admission_no=info.get("admission_no")).one_or_none():
        abort(400, f"User with admission no {info.get('admission_no')} exist")
    student = Student()
    for k, v in info.items():
        if hasattr(Student, k):
            if k == "dob":
                try:
                    v = date.fromisoformat(v)
                except ValueError:
                    continue
            setattr(student, k, v)
    student.save()
    return jsonify(student.to_dict()), 201
    
@portal.route("/students/<student_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
@swag_from('../documentations/portal/student/student_id.yml', methods=['GET', 'PUT', 'DELETE'])
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
    if request.method == "GET":
        return jsonify(student.to_dict()), 200
    
    # Only teacher who is an admin can DELETE and PUT.
    # The teacher must have admin privileges
    user_id = request.current_user.id
    # Get the teacher instance
    teacher = Teacher.get(user_id)
    if teacher is None:
        #not a teacher, permission denied
        abort(401)
    if teacher.isAdmin() is False:
        abort(401)
    admin = Admin.query.filter(Admin.teacher_id==user_id).one_or_none()
    if admin is None:
        abort(401)
    
    if admin.privileges is None:
        abort(401)

# DELETE method
    if request.method == "DELETE":
        if admin.privileges.get("delete") is False:
            abort(401)
        student.delete()
        return jsonify({}), 204
 
 # PUT method   
    if admin.privileges.get("update") is False:
        abort(401)
    
    info = request.get_json(silent=True)
    if info is None:
        abort(400, "Not a JSON")
    for k, v in info.items():
        if k not in ["created_at", "id"] and hasattr(Student, k):
            if k == "dob":
                try:
                    v = date.fromisoformat(v)
                except ValueError:
                    return jsonify({"Error": f"wrong {k} date format"}), 400 
            if k =="username":
                if User.query.filter_by(username=v).one_or_none():
                    return jsonify({f"User with {v} exist"}), 400
            if k =="email":
                if User.query.filter_by(email=v).one_or_none():
                    return jsonify({f"User with {v} exist"}), 400
            setattr(student, k, v)
    student.save()
    return jsonify(student.to_dict()), 202
