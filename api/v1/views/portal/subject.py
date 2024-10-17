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

@portal.route("/subjects/", methods=["GET", "POST"], strict_slashes=False)
def subjects():
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
        paginate = Subject.paginate(page=page, per_page=per_page)
        count, subjects, next_page = paginate
        results = {
            "page": page,
            "total": count,
            "per_page": per_page,
            "next_page": next_page,
            "results": [subject.to_dict() for subject in subjects.all()]
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
    
    if not info.get("name"):
        abort(400, "Missing name")
    if not info.get("code"):
        abort(400, "Missing code")
    subject = Subject()
    for k, v in info.items():
        if k != "id" and hasattr(Subject, k):
            if k in ["dob"]:
                try:
                    v = date.fromisoformat(v)
                except ValueError:
                    continue 
            setattr(subject, k, v)
    subject.save()
    return jsonify(subject.to_dict()), 201

@portal.route("/subjects/<subject_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def subject(subject_id):

    # ge subject by id
    subject = Subject.query.filter_by(id=subject_id).one_or_none()
    if not subject:
        # get subject by code
        subject = Subject.query.filter_by(code=subject_id).one_or_none()
        if subject is None:
            # if subject does not exist
            abort(404)
 # GET method
    if request.method == "GET":
        return jsonify(subject)
    
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
        subject.delete()
        return jsonify({}), 204
 
 # PUT method   
    if admin.privileges.get("update") is False:
        abort(403)
    
    info = request.get_json(silent=True)
    if info is None:
        abort(400, "Not a JSON")
    if info.get("name"):
        name = info.get("name")
        query = Subject.query.filter_by(name=name)
        if query.where(Subject.id!=subject.id).one_or_none():
            msg = {f"subject of with name: {name} exist"}
            return jsonify(msg)
    if info.get("code"):
        code = info.get("code")
        query = Subject.query.filter_by(code=code)
        if query.where(Subject.id!=subject.id).one_or_none():
            msg = {f"subject of with name: {code} exist"}
            return jsonify(msg)
    for k, v in info.items():
        if k not in ["created_at", "id"] and hasattr(Subject, k):    
            setattr(subject, k, v)
    subject.save()
    return jsonify(subject.to_dict()), 201

@portal.route("/subjects/<subject_id>/courses", methods=["GET", "PUT"], strict_slashes=False)
def subject_courses(subject_id):
    # ge subject by id
    subject = Subject.query.filter_by(id=subject_id).one_or_none()
    if not subject:
        # get subject by code
        subject = Subject.query.filter_by(code=subject_id).one_or_none()
        if subject is None:
            # if subject does not exist
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
        if offset >= length:
            abort(400)
        remain = length - offset
        end = offset + perpg if remain >= perpg else offset + remain
        children = {
            
              "page": page,
              "total": len(subject.courses),
              "next_page": page + 1 if page * perpg < len(subject.courses) else 1
            ,

            "courses": [{
            subject.courses[i].to_dict()
            } for i in  range(offset, end)]
        }
        return jsonify(children), 200
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
    subject.courses.append(Course.get(course_id))
    subject.save()
    return jsonify(subject.to_dict()), 201
   
