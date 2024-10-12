"""parent endpoints
"""
from flask import abort, jsonify, request
from api.v1.views.portal import portal
from models.portal.parent import Parent


@portal.route("parent/<parent_id>", methods=["GET"])
def parents(parent_id):
    """retrieve parent wth given id i.e parent_id
    

    Args:
        parent_id (str): id of parent to retrieve or
    """
    parent = Parent.get(parent_id)
    if not parent:
    # if parent does not exist
        abort(404)

    # To retrieve parent
    return jsonify(parent.to_dict())
