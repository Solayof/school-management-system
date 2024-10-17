"""student route
"""
from datetime import date
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
def students():
    """student route
        GET: get all students default limit of 10 student
        POST: create new student
    """
    if request.method == "GET":
        try:
            page = abs(int( request.args.get("page", 1)))
        except ValueError:
            return jsonify({"page": "page number not an intiger"}), 422
        try:
            per_page = abs(int(request.args.get("per_page", 10)))
        except ValueError:
            return jsonify({"per_page": "number per page not an intiger"}), 422
        print(page, per_page)
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
    # Only teacher who is an admin with creat privilege can POST.
    # The teacher must have admin privileges
    user_id = request.current_user.id
    # Get the teacher instance
    teacher = Teacher.get(user_id)
    if teacher is None:
        #not a teacher, permission denied
        abort(403)
    if teacher.isAdmin() is False:
        abort(403)
    print(teacher)
    admin = Admin.query.filter(Admin.teacher_id==user_id).one_or_none()
    if admin is None:
        abort(403)
    
    if admin.privileges is None:
        abort(403)
    if admin.privileges.get("create") is False:
        return jsonify({"CREATE PERMISSION DENIED"}), 403
    info = request.get_json(silent=True)
    if info is None:
        abort(400, "Not a JSON")
    
    if not info.get("username"):
        abort(400, "Missing username")
    if User.query.filter_by(username=info.get("username")).one_or_none():
        abort(400, f"User with {info.get('username')} exist")
    if not info.get("email"):
        abort(400, "Missing email")
    if User.query.filter_by(username=info.get("email")).one_or_none():
        abort(400, f"User with {info.get('email')} exist")
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
def student(student_id=None):
    """retrieve student wth given id i.e student_id
    

    Args:
        student_id (str): id of student to retrieve or
    """
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
        abort(403)
    if teacher.isAdmin() is False:
        abort(403)
    admin = Admin.query.filter(Admin.teacher_id==user_id).one_or_none()
    if admin is None:
        abort(403)
    
    if admin.privileges is None:
        abort(403)

# DELETE method
    if request.method == "DELETE":
        if admin.privileges.get("delete") is False:
            abort(403)
        student.delete()
        return jsonify({}), 204
 
 # PUT method   
    if admin.privileges.get("update") is False:
        abort(403)
    
    info = request.get_json(silent=True)
    if info is None:
        abort(400, "Not a JSON")
    for k, v in info.items():
        if k not in ["created_at", "id"] and hasattr(Student, k):
            if k == "dob":
                try:
                    v = date.fromisoformat(v)
                except ValueError:
                    continue 
            if k =="username":
                if User.query.filter_by(username=v).one_or_none():
                    return jsonify({f"User with {v} exist"}), 422
            if k =="email":
                if User.query.filter_by(email=v).one_or_none():
                    return jsonify({f"User with {v} exist"}), 422
            setattr(student, k, v)
    student.save()
    return jsonify(student.to_dict()), 201
