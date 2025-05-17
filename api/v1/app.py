"""school flask API

    Returns:
        json: return json
"""
from flasgger import Swagger
from flask import abort, Flask, jsonify, request
from flask_cors import CORS
from os import getenv
from api.v1.auth.session_db_auth import SessionDbAuth
from api.v1.views.admin import admin
from api.v1.views.cbt import cbt
from api.v1.views.portal import portal
from models import storage


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(admin)
app.register_blueprint(cbt)
app.register_blueprint(portal)
CORS(app, resources={r"/*": {"origins": ['http:localhost:4200']}})


auth = SessionDbAuth()

@app.before_request
def request_filter():
    excluded_paths = [
        '/api/portal/auth_session/login/',
        '/apidocs/',
        '/api/portal/apidocs/',
        '/flasgger_static/*',
        '/apispec_1.json'
    ]
    if auth and auth.require_auth(request.path, excluded_paths):
        cookie = auth.session_cookie(request)
        if auth.authentication_header(request) is None and cookie is None:
            abort(401)

        if auth.current_user(request) is None:
            abort(403)
        request.current_user = auth.current_user(request)

@app.errorhandler(401)
def unauthorized(error):
    return jsonify(
        {"error": "Unauthorized"}
    ), 401
    
@app.errorhandler(400)
def unauthorized(error):
    return jsonify(
        {"error": "Bad request"}
    ), 400

@app.errorhandler(403)
def forbiden(error):
    return jsonify({
        "error": "Forbidden"
    }), 403

@app.errorhandler(404)
def not_found(error):
    return jsonify(
        {"error": "Not found"}
    ), 404
    

@app.teardown_appcontext
def teardown_storage(exc):
    storage.close()
    
Swagger(app)
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )
