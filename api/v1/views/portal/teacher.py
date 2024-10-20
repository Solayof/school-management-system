"""teacher endpoints
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

@portal.route("/teachers", methods=["GET", "POST"], strict_slashes=False)
def teachers():
    """teacher route
        GET: get all teachers default limit of 10 teacher
        POST: create new teacher
    """
    if request.method == "GET":
        try:
            page = abs(int( request.args.get("page", 1)))
        except ValueError:
            abort(400)
        try:
            per_page = abs(int(request.args.get("per_page", 1)))
        except ValueError:
            abort(400)
        if page <= 0 or per_page <= 0:
            return abort(400)
        paginate = Teacher.paginate(page=page, per_page=per_page)
        count, teachers, next_page = paginate
        results = {
            "page": page,
            "total": count,
            "per_page": per_page,
            "next_page": next_page,
            "results": [teacher.to_dict() for teacher in teachers.all()]
        }
        return jsonify(results), 200

# POST method
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
    teacher = Teacher()
    for k, v in info.items():
        if k != "id" and hasattr(Teacher, k):
            if k in ["dob", "date_transfer", "last_promote_date"]:
                try:
                    v = date.fromisoformat(v)
                except ValueError:
                    continue 
            setattr(teacher, k, v)
    teacher.save()
    return jsonify(teacher.to_dict()), 201
    
@portal.route("/teachers/<teacher_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
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
    if request.method == "GET":
        return jsonify(teacher.to_dict()), 200
    
    # Only teacher who is an admin can DELETE and PUT.
    # The teacher must have admin privileges
    user_id = request.current_user.id
    # Get the teacher instance
    tea = Teacher.get(user_id)
    if tea is None:
        #not a teacher, permission denied
        abort(403)
    if tea.isAdmin() is False:
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
        if teacher.isAdmin() is True:
            ad = Admin.query.filter(Admin.teacher_id==teacher.id).one_or_none()
            ad.delete()
        teacher.delete()
        return jsonify({}), 204
 
 # PUT method   
    if admin.privileges.get("update") is False:
        abort(403)
    
    info = request.get_json(silent=True)
    if info is None:
        abort(400, "Not a JSON")
    for k, v in info.items():
        if k not in ["created_at", "id"] and hasattr(Teacher, k):
            if k in ["dob", "date_transfer", "last_promote_date"]:
                try:
                    v = date.fromisoformat(v)
                except ValueError:
                    continue
            if k =="username":
                if User.query.filter_by(username=v).one_or_none():
                    return jsonify({f"User with {v} exist"}), 400
            if k =="email":
                if User.query.filter_by(email=v).one_or_none():
                    return jsonify({f"User with {v} exist"}), 400
            setattr(teacher, k, v)
    teacher.save()
    return jsonify(teacher.to_dict()), 201

@portal.route("/teachers/<teacher_id>/courses", methods=["GET", "PUT"], strict_slashes=False)
def teacher_courses(teacher_id):
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
    
    if request.method == "GET":
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
    # Only teacher who is an admin with update privilege can POST.
    # The teacher must have admin privileges
    user_id = request.current_user.id
    # Get the teacher instance
    tea = Teacher.get(user_id)
    if tea is None:
        #not a teacher, permission denied
        abort(403)
    if tea.isAdmin() is False:
        abort(403)
    admin = Admin.query.filter(Admin.teacher_id==user_id).one_or_none()
    if admin is None:
        abort(403)
    
    if admin.privileges is None:
        abort(403)
    if admin.privileges.get("update") is False:
        return jsonify({"UPDATE PERMISSION DENIED"}), 422
    course_id = request.args.get("courseId")
    
    if Course.get(course_id) is None:
        return jsonify(f"No course with {course_id} as id"), 404
    teacher.courses.append(Course.get(course_id))
    teacher.save()
    return jsonify(teacher.to_dict()), 201
