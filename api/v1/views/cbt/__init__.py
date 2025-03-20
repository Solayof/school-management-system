"""CBT Bluerint
    all the cbr route are define here
"""
from flask import Blueprint
from flask_cors import CORS


cbt = Blueprint("cbt", __name__, url_prefix="/api/cbt")
CORS(cbt, supports_credentials=True, origins=["http://localhost:4200"])
from api.v1.views.cbt.examination import *
from api.v1.views.cbt.question import *
from api.v1.views.cbt.response import *
from api.v1.views.cbt.score import *
from api.v1.views.cbt.option import *
