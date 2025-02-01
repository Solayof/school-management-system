"""CBT Bluerint
    all the cbr route are define here
"""
from flask import Blueprint


cbt = Blueprint("cbt", __name__, url_prefix="/api/cbt")
from api.v1.views.cbt.examination import *
from api.v1.views.cbt.question import *
from api.v1.views.cbt.response import *
from api.v1.views.cbt.score import *
from api.v1.views.cbt.option import *
