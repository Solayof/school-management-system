"""admin Bluerint
    all the admin route are define here
"""
from flask import Blueprint, request
from models.portal.admin import Admin as Adm


admin = Blueprint("admin", __name__, url_prefix="/api/admin")
@admin.before_request
def admin_filter():
    if request.current_user.isAdmin() is False:
        abort(401)
    request.admin = Adm.query.filter_by(teacher_id=request.current_user.id).one_or_none()


from api.v1.views.admin.admins import *
from api.v1.views.admin.examination import *
from api.v1.views.admin.option import *
from api.v1.views.admin.question import *
from api.v1.views.admin.course import *
from api.v1.views.admin.admission import *
from api.v1.views.admin.Class import *
from api.v1.views.admin.parent import *
from api.v1.views.admin.response import *
from api.v1.views.admin.score import *
from api.v1.views.admin.student import *
from api.v1.views.admin.subject import *
from api.v1.views.admin.teacher import *