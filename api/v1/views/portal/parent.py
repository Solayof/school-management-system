"""parent endpoints
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


@portal.route("/parents/<parent_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def parent(parent_id=None):
    """retrieve parent wth given id i.e parent_id
    

    Args:
        parent_id (str): id of parent to retrieve or
    """
    # ge parent by id
    parent = Parent.query.filter_by(id=parent_id).one_or_none()
    if not parent:
        # get parent by username
        parent = Parent.query.filter_by(username=parent_id).one_or_none()
        if parent is None:
            # Get parent by email
            parent = Parent.query.filter_by(email=parent_id).one_or_none()
            if parent is None:
                 # if parent does not exist
                abort(404)
    if request.method == "GET":
        # To retrieve parent
        return jsonify(parent.to_dict()), 200
    
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
    admin = Admin.query.filter(Admin.teacher_id==user_id)
    if admin is None:
        abort(403)
    
    if admin.privileges is None:
        abort(403)
    
    if request.method == "DELETE":
        if admin.privileges.get("delete") is False:
            abort(403)
        parent.delete()
        return jsonify({}), 204
    
    if admin.privileges.get("update") is False:
        abort(403)
    
    info = request.get_json(silent=True)
    if info is None:
        abort(400, "Not a JSON")
    for k, v in info.items():
        if k not in ["created_at", "id"] and hasattr(Parent, k):
            if k == "dob":
                try:
                    v = date.fromisoformat(v)
                except ValueError:
                    return jsonify({"Error": f"wrong {k} date format"})
            if k =="username":
                if User.query.filter_by(username=v).one_or_none():
                    return jsonify({f"User with {v} exist"}), 422
            if k =="email":
                if User.query.filter_by(email=v).one_or_none():
                    return jsonify({f"User with {v} exist"}), 422
            setattr(parent, k, v)
    parent.save()
    return jsonify(parent.to_dict()), 201
        

@portal.route("/parents", methods=["GET", "POST"])
def parents():
    """parent route
        GET: get all parents default limit of 10 parent
        POST: create new parent
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
        paginate = Parent.paginate(page=page, per_page=per_page)
        count, parents, next_page = paginate
        results = {
            "page": page,
            "total": count,
            "per_page": per_page,
            "next_page": next_page,
            "results": [parent.to_dict() for parent in parents.all()]
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
    admin = Admin.query.filter(Admin.teacher_id==user_id)
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
    parent = Parent()
    for k, v in info.items():
        if k != "id" and hasattr(Parent, k):
            if k == "dob":
                try:
                    v = date.fromisoformat(v)
                except ValueError:
                    return jsonify({"Error": f"wrong {k} date format"})
            setattr(parent, k, v)
    parent.save()
    return jsonify(parent.to_dict()), 201
    
@portal.route("/parents/<parent_id>/children", methods=["GET", "POST"], strict_slashes=False)
def children(parent_id=None):
    """retrieve parent wth given id i.e parent_id
    

    Args:
        parent_id (str): id of parent to retrieve or
    """
    # ge parent by id
    parent = Parent.query.filter_by(id=parent_id).one_or_none()
    if not parent:
        # get parent by username
        parent = Parent.query.filter_by(username=parent_id).one_or_none()
        if parent is None:
            # Get parent by email
            parent = Parent.query.filter_by(email=parent_id).one_or_none()
            if parent is None:
                 # if parent does not exist
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

        children = [
            {
                "page": page,
                "total": len(parent.children),
                "next_page": page + 1 if page * perpg < len(parent.children) else 1
            },

            [{
            parent.children[i].to_dict()
            } for i in  range(offset, end)]
        ]
        return jsonify(children), 200
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
    admin = Admin.query.filter(Admin.teacher_id==user_id)
    if admin is None:
        abort(403)
    
    if admin.privileges is None:
        abort(403)
    if admin.privileges.get("create") is False:
        return jsonify({"CREATE PERMISSION DENIED"}), 422
    info = request.get_json(silent=True)
    if info is None:
        abort(400, "Not a JSON")
    if not info.get("arm"):
        abort(400, "Missing arm")
    if not info.get("username"):
        abort(400, "Missing username")
    if User.query.filter_by(username=info.get("username")).one_or_none():
        abort(400, f"User with {info.get('username')} exist")
    if not info.get("email"):
        abort(400, "Missing email")
    if User.query.filter_by(email=info.get("email")).one_or_none():
        abort(400, f"User with {info.get('email')} exist")
    if not info.get("admission_no"):
        abort(400, "Missing admission no")
    admission_no = info.get("admission_no")
    if User.query.filter_by(admission_no=admission_no).one_or_none():
        abort(400, f"User with {info.get('admission_no')} exist")
    
    student = Student()
    for k, v in info.items():
        if k != "id" and hasattr(Student, k):
            if k == "dob":
                try:
                    v = date.fromisoformat(v)
                except ValueError:
                   continue  
            setattr(student, k, v)
    student.parent_id = parent.id
    student.save()
    return jsonify(student.to_dict()), 201
