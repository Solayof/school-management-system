"""admin Bluerint
    all the admin route are define here
"""
from flask import Blueprint


admin = Blueprint("admin", __name__, url_prefix="/api/admin")
from api.v1.views.cbt.examination import *
from api.v1.views.cbt.question import *
from api.v1.views.cbt.response import *
from api.v1.views.cbt.score import *
