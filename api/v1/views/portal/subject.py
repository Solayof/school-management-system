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

@portal.route("/subjects/", methods=["GET"], strict_slashes=False)
def subjects():
    """Retrrieve subjects or create subject

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

@portal.route("/subjects/<subject_id>", methods=["GET"], strict_slashes=False)
def subject(subject_id):
    """Retrieve, update or delete specific subject

    Args:
        subject_id (str): subject id or code to retrieve, update or delete
    """    
    # ge subject by id
    subject = Subject.query.filter_by(id=subject_id).one_or_none()
    if not subject:
        # get subject by code
        subject = Subject.query.filter_by(code=subject_id).one_or_none()
        if subject is None:
            # if subject does not exist
            abort(404)
 # GET method
    return jsonify(subject)

@portal.route("/subjects/<subject_id>/courses", methods=["GET"], strict_slashes=False)
def subject_courses(subject_id):
    """Retrieve courses or assign course to the subject or create course.

    Args:
        subject_id (str): id or code of the subject to retrieve its courses, assign course or create course

    Returns:
        json: json response
    """    
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
            abort(400)
        try:
            perpg = abs(int(request.args.get("per_page", 10)))
        except ValueError:
            abort(400)
        if perpg == 0  or page == 0:
            abort(400)
        offset = (page - 1) * perpg
        length = len(subject.courses)
        if offset >= length:
            abort(400)
        remain = length - offset
        end = offset + perpg if remain >= perpg else offset + remain
        children = [{
            
              "page": page,
              "total": len(subject.courses),
              "next_page": page + 1 if page * perpg < len(subject.courses) else 1
        },

            [
            subject.courses[i].to_dict()
             for i in  range(offset, end)]
        ]
        return jsonify(children), 200