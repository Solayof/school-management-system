"""portal Bluerint
    all the portal route are define here
"""
from flask import Blueprint
from flask_cors import CORS


portal = Blueprint("portal", __name__, url_prefix="/api/portal")
CORS(portal, supports_credentials=True, origins=["http://localhost:4200"])
from api.v1.views.portal.Class import *
from api.v1.views.portal.course import *
from api.v1.views.portal.parent import *
from api.v1.views.portal.student import *
from api.v1.views.portal.subject import *
from api.v1.views.portal.teacher import *
from api.v1.views.session_auth import *
