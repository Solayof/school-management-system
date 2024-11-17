"""admin Bluerint
    all the admin route are define here
"""
from flask import Blueprint


admin = Blueprint("admin", __name__, url_prefix="/api/admin")
from api.v1.views.admin.admins import *