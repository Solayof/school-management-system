#!/usr/bin/python3
"initialzing db"
from models.engine.storage import Dbstorage
# from models.portal.admin import Admin

storage = Dbstorage()
storage.init()