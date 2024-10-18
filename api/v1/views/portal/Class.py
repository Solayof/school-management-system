from datetime import date
from flask import abort, jsonify, request
from sqlalchemy import and_
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

@portal.route("/classes/", methods=["GET", "POST"], strict_slashes=False)
def classes():
    """get all classes or create a class

    Returns:
        json: response
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
        paginate = Class.paginate(page=page, per_page=per_page)
        count, classes, next_page = paginate
        results = {
            "page": page,
            "total": count,
            "per_page": per_page,
            "next_page": next_page,
            "results": [clas.to_dict() for clas in classes.all()]
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
    
    if not info.get("className"):
        abort(400, "Missing class name")

    clas = Class(className=info.get("className"))

    clas.save()
    return jsonify(clas.to_dict()), 201

@portal.route("/classes/<clas_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def clas(clas_id):
    """get, update and delete specific class

    Args:
        clas_id (str): id od code of the class to get update or delete
    """    
    # ge class by id
    clas = Class.query.filter_by(id=clas_id).one_or_none()
    if not clas:
        # get class by code
        clas = Class.query.filter_by(code=clas_id).one_or_none()
        if clas is None:
            # if class does not exist
            abort(404)
 # GET method
    if request.method == "GET":
        return jsonify(clas.to_dict())
    
     # Only teacher who is an admin can DELETE and PUT.
    # The teacher must have admin privileges
    user_id = request.current_user.id
    # Get the teacher instance
    teacher = Teacher.get(user_id)
    if teacher is None:
        #not a teacher, permission denied
        return jsonify({"Not a teacher"})
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
            return jsonify({"delete permission denied"}), 403
        clas.delete()
        return jsonify({}), 204
 
 # PUT method   
    if admin.privileges.get("update") is False:
        return jsonify({"update permission deneid"}), 403
    
    info = request.get_json(silent=True)
    if info is None:
        abort(400, "Not a JSON")

    if info.get("code"):
        code = info.get("code")
        query = Class.query.filter_by(code=code)
        if query.where(Class.id!=clas.id).one_or_none():
            msg = {f"class of with name: {code} exist"}
            return jsonify(msg)
    for k, v in info.items():
        if k not in ["created_at", "id"] and hasattr(Class, k):    
            setattr(clas, k, v)
    clas.save()
    return jsonify(clas.to_dict()), 201

@portal.route("/classes/<clas_id>/courses", methods=["GET", "PUT"], strict_slashes=False)
def class_courses(clas_id):
    """get and update a specific class course

    Args:
        clas_id (str): id or code of the class to get or update its course
    """    
    # ge clas by id
    clas = Class.query.filter_by(id=clas_id).one_or_none()
    if not clas:
        # get clas by code
        clas = Class.query.filter_by(code=clas_id).one_or_none()
        if clas is None:
            # if clas does not exist
            abort(404)
    
    if request.method == "GET":
        try:
            page = abs(int( request.args.get("page", 1)))
        except ValueError:
            return jsonify({"page": "page number not an intiger"}), 422
        try:
            perpg = abs(int(request.args.get("per_page", 10)))
        except ValueError:
            return jsonify({"per_page": "number per page not an intiger"}), 422

        if perpg == 0  or page == 0:
            abort(400)
        offset = (page - 1) * perpg
        length = len(clas.courses)
        if offset >= length and length is not 0:
            abort(404)
        remain = length - offset
        end = offset + perpg if remain >= perpg else offset + remain

        courses = {
            
              "page": page,
              "total": len(clas.courses),
              "next_page": page + 1 if page * perpg < len(clas.courses) else 1
            ,

            "courses": [{
            clas.courses[i].to_dict()
            } for i in  range(offset, end)]
        }
        return jsonify(courses), 200
    # Only teacher who is an admin with update privilege can POST.
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
    if admin.privileges.get("update") is False:
        return jsonify({"UPDATE PERMISSION DENIED"}), 422
    course_id = request.args.get("courseId")
    
    if Course.get(course_id) is None:
        return jsonify(f"No course with {course_id} as id"), 404
    clas.courses.append(Course.get(course_id))
    clas.save()
    return jsonify(clas.to_dict()), 201


@portal.route("/classes/<clas_id>/form_teacher", methods=["GET", "PUT"], strict_slashes=False)
def class_form_teacher(clas_id):
    # ge clas by id
    clas = Class.query.filter_by(id=clas_id).one_or_none()
    if not clas:
        # get clas by code
        clas = Class.query.filter_by(code=clas_id).one_or_none()
        if clas is None:
            # if clas does not exist
            abort(404)
    
    if request.method == "GET":
        try:
            page = abs(int( request.args.get("page", 1)))
        except ValueError:
            return jsonify({"page": "page number not an intiger"}), 422
        try:
            perpg = abs(int(request.args.get("per_page", 10)))
        except ValueError:
            return jsonify({"per_page": "number per page not an intiger"}), 422
        
        if perpg == 0  or page == 0:
            abort(400)
        offset = (page - 1) * perpg
        length = len(teacher.course)
        if offset >= length and length is not 0:
            abort(404)
        remain = length - offset
        end = offset + perpg if remain >= perpg else offset + remain

        form_teacher = {
            
              "page": page,
              "total": len(clas.form_teacher),
              "next_page": page + 1 if page * perpg < len(clas.form_teacher) else 1
            ,

            "courses": [{
            clas.form_teacher[i].to_dict()
            } for i in  range(offset, end)]
        }
        return jsonify(form_teacher), 200
    # Only teacher who is an admin with update privilege can POST.
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
    if admin.privileges.get("update") is False:
        return jsonify({"UPDATE PERMISSION DENIED"}), 422
    teacher_id = request.args.get("teacherId")
    
    if Teacher.get(teacher_id) is None:
        return jsonify(f"No course with {teacher_id} as id"), 404
    clas.form_teacher.append(Teacher.get(teacher_id))
    clas.save()
    return jsonify(clas.to_dict()), 201


@portal.route("/classes/<clas_id>/students", methods=["GET", "PUT"], strict_slashes=False)
def class_students(clas_id):
    # ge clas by id
    clas = Class.query.filter_by(id=clas_id).one_or_none()
    if not clas:
        # get clas by code
        clas = Class.query.filter_by(code=clas_id).one_or_none()
        if clas is None:
            # if clas does not exist
            abort(404)
    
    if request.method == "GET":
        try:
            page = abs(int( request.args.get("page", 1)))
        except ValueError:
            return jsonify({"page": "page number not an intiger"}), 422
        try:
            perpg = abs(int(request.args.get("per_page", 10)))
        except ValueError:
            return jsonify({"per_page": "number per page not an intiger"}), 422
        
        if perpg == 0  or page == 0:
            abort(400)
        offset = (page - 1) * perpg
        length = len(teacher.course)
        if offset >= length and length is not 0:
            abort(404)
        remain = length - offset
        end = offset + perpg if remain >= perpg else offset + remain
        students = {
            
              "page": page,
              "total": len(clas.students),
              "next_page": page + 1 if page * perpg < len(clas.students) else 1
            ,

            "courses": [{
            clas.students[i].to_dict()
            } for i in  range(offset, end)]
        }
        return jsonify(students), 200
    # Only teacher who is an admin with update privilege can POST.
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
    if admin.privileges.get("update") is False:
        return jsonify({"UPDATE PERMISSION DENIED"}), 422
    student_id = request.args.get("studentId")
    
    if Student.get(student_id) is None:
        return jsonify(f"No course with {student_id} as id"), 404
    clas.students.append(Student.get(student_id))
    clas.save()
    return jsonify(clas.to_dict()), 201


@portal.route("/classes/<clas_id>/examinations", methods=["GET", "PUT"], strict_slashes=False)
def class_examinations(clas_id):
    # ge clas by id
    clas = Class.query.filter_by(id=clas_id).one_or_none()
    if not clas:
        # get clas by code
        clas = Class.query.filter_by(code=clas_id).one_or_none()
        if clas is None:
            # if clas does not exist
            abort(404)
    
    if request.method == "GET":
        try:
            page = abs(int( request.args.get("page", 1)))
        except ValueError:
            return jsonify({"page": "page number not an intiger"}), 422
        try:
            perpg = abs(int(request.args.get("per_page", 10)))
        except ValueError:
            return jsonify({"per_page": "number per page not an intiger"}), 422
        
        if perpg == 0  or page == 0:
            abort(400)
        offset = (page - 1) * perpg
        length = len(teacher.course)
        if offset >= length and length != 0:
            abort(404)
        remain = length - offset
        end = offset + perpg if remain >= perpg else offset + remain
        examinations = {
            
              "page": page,
              "total": len(clas.examinations),
              "next_page": page + 1 if page * perpg < len(clas.examinations) else 1
            ,

            "courses": [{
            clas.examinations[i].to_dict()
            } for i in  range(offset, end)]
        }
        return jsonify(examinations), 200
    # Only teacher who is an admin with update privilege can POST.
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
    if admin.privileges.get("update") is False:
        return jsonify({"UPDATE PERMISSION DENIED"}), 422
    examination_id = request.args.get("examinationId")
    
    if Examination.get(examination_id) is None:
        return jsonify(f"No course with {examination_id} as id"), 404
    clas.examinations.append(Examination.get(examination_id))
    clas.save()
    return jsonify(clas.to_dict()), 202
