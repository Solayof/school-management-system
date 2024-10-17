"""portal Bluerint
    all the portal route are define here
"""
from flask import Blueprint


portal = Blueprint("portal", __name__, url_prefix="/api/portal")
from api.v1.views.admin.admin import *
from api.v1.views.portal.Class import *
from api.v1.views.portal.course import *
from api.v1.views.portal.parent import *
from api.v1.views.portal.student import *
from api.v1.views.portal.subject import *
from api.v1.views.portal.teacher import *
from api.v1.views.session_auth import *
