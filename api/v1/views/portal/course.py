"""Course endpoints
"""
from datetime import date
from flask import abort, jsonify, request
from sqlalchemy import and_
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

@portal.route("/courses/", methods=["GET"], strict_slashes=False)
def courses():
    """retrieve courses and create course

    Returns:
        json: json response
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
        paginate = Course.paginate(page=page, per_page=per_page)
        count, courses, next_page = paginate
        results = {
            "page": page,
            "total": count,
            "per_page": per_page,
            "next_page": next_page,
            "results": [course.to_dict() for course in courses.all()]
        }
        return jsonify(results), 200

@portal.route("/courses/<course_id>", methods=["GET"], strict_slashes=False)
def course(course_id):
    """retrieve, update and delete specific courses

    Args:
        course_id (str): the id of the course to retrieve, update and delete
    """
    # ge course by id
    course = Course.query.filter_by(id=course_id).one_or_none()
    if not course:
        # if course does not exist
        abort(404)
 # GET method
    if request.method == "GET":
        return jsonify(course)
    


@portal.route("/courses/<course_id>/questions", methods=["GET"], strict_slashes=False)
def courses_courses(course_id):
    """Retrieve, and upadte specific course questions

    Args:
        course_id (str): the id of the course to retreive or update its questions

    Returns:
        json: json response
    """    
    # ge courses by id
    course = Course.query.filter_by(id=course_id).one_or_none()
    if not course:
        # if course does not exist
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
        
        if perpg <= 0  or page <= 0:
            abort(400)
        offset = (page - 1) * perpg
        length = len(course.questions)
        if offset >= length and length != 0:
            abort(404)
        remain = length - offset
        end = offset + perpg if remain >= perpg else offset + remain
        questions = [{
            
              "page": page,
              "total": len(course.questions),
              "next_page": page + 1 if page * perpg < len(course.questions) else 1
        },
            [
            course.questions[i].to_dict()
             for i in  range(offset, end)]
        ]
        return jsonify(questions), 200


@portal.route("/courses/<course_id>/teachers", methods=["GET"], strict_slashes=False)
def courses_teachers(course_id):
    """Retrieve, and upadte specific course teachers

    Args:
        course_id (str): the id of the course to retreive or update its teachers

    Returns:
        json: json response
    """ 
    # ge course by id
    course = Course.query.filter_by(id=course_id).one_or_none()
    if not course:
        # if course does not exist
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
        
        if perpg <= 0  or page <= 0:
            abort(400)
        offset = (page - 1) * perpg
        length = len(course.teachers)
        if offset >= length and length != 0:
            abort(404)
        remain = length - offset
        end = offset + perpg if remain >= perpg else offset + remain
        teachers = [{
            
              "page": page,
              "total": len(course.teachers),
              "next_page": page + 1 if page * perpg < len(course.teachers) else 1
        },

            [
            course.teachers[i].to_dict()
             for i in  range(offset, end)]
        ]
        return jsonify(teachers), 200


@portal.route("/courses/<course_id>/students", methods=["GET"], strict_slashes=False)
def courses_students(course_id):
    """Retrieve, and upadte specific course students

    Args:
        course_id (str): the id of the course to retreive or update its students

    Returns:
        json: json response
    """ 
    # ge course by id
    course = Course.query.filter_by(id=course_id).one_or_none()
    if not course:
        # if course does not exist
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
        
        if perpg <= 0  or page <= 0:
            abort(400)
        offset = (page - 1) * perpg
        length = len(course.students)
        if offset >= length and length != 0:
            abort(404)
        remain = length - offset
        end = offset + perpg if remain >= perpg else offset + remain
        students = [{
            
              "page": page,
              "total": len(course.students),
              "next_page": page + 1 if page * perpg < len(course.students) else 1
        },

            [
            course.students[i].to_dict()
             for i in  range(offset, end)]
        ]
        return jsonify(students), 200

@portal.route("/courses/<course_id>/examinations", methods=["GET"], strict_slashes=False)
def courses_examinations(course_id):
    """Retrieve, and upadte specific course examinations

    Args:
        course_id (str): the id of the course to retreive or update its examinations

    Returns:
        json: json response
    """ 
    # ge course by id
    course = Course.query.filter_by(id=course_id).one_or_none()
    if not course:
        # if course does not exist
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
        
        if perpg <= 0  or page <= 0:
            abort(400)
        offset = (page - 1) * perpg
        length = len(course.examinations)
        if offset >= length and length != 0:
            abort(404)
        remain = length - offset
        end = offset + perpg if remain >= perpg else offset + remain
        examinations = [{
            
              "page": page,
              "total": len(course.examinations),
              "next_page": page + 1 if page * perpg < len(course.examinations) else 1
        },

            [
            course.examinations[i].to_dict()
             for i in  range(offset, end)]
        ]
        return jsonify(examinations), 200
    

@portal.route("/courses/<course_id>/classes", methods=["GET"], strict_slashes=False)
def courses_classes(course_id):
    """Retrieve, and upadte specific course classes

    Args:
        course_id (str): the id of the course to retreive or update its classes

    Returns:
        json: json response
    """ 
    # ge course by id
    course = Course.query.filter_by(id=course_id).one_or_none()
    if not course:
        # if course does not exist
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
        length = len(course.classes)
        if offset >= length:
            abort(400)
        remain = length - offset
        end = offset + perpg if remain >= perpg else offset + remain
 
        classes = [{
            
              "page": page,
              "total": len(course.classes),
              "next_page": page + 1 if page * perpg < len(course.classes) else 1
        },

            [
            course.classes[i].to_dict()
             for i in  range(offset, end)]
        ]
        return jsonify(classes), 200
    