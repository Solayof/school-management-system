"""portal Bluerint
    all the portal route are define here
"""
from flask import Blueprint
from flask_cors import CORS


elearn = Blueprint("portal", __name__, url_prefix="/api/portal")
CORS(elearn, supports_credentials=True, origins=["http://localhost:4200"])

