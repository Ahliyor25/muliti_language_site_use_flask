"""
Module Utils.py
A set of functions that are needed for the project
"""


import json
import os

from flask.json import jsonify
from models import Ids
from peewee import *
from hashlib import sha256
from werkzeug.utils import find_modules, import_string


class helper_var:
    host = "http://192.168.0.103:3000/getimg/"
    path = 'C:\\bahtz\\muliti_language_site_use_flask'





# * Blueprints


def register_blueprints_login(app):
    """
    Searches all blueprints in folder blueprints/login
    """
    for name in find_modules('blueprints.login'):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            app.register_blueprint(mod.bp)

def register_blueprints_main_page(app):
    """
    Searches all blueprints in folder blueprints/main_page
    """
    for name in find_modules('blueprints.main_page'):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            app.register_blueprint(mod.bp)

def register_blueprints_residence(app):
    """
    Searches all blueprints in folder blueprints/residence
    """
    for name in find_modules('blueprints.residence'):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            app.register_blueprint(mod.bp)


def hash_string_sha256(to_hash):
    """
    Hashes string to sha256
    """
    return sha256(to_hash.encode()).hexdigest()


def upload_image(files):
    """
    Upload image use form data
    """
    target = os.path.join(helper_var.path, 'images')
    if not os.path.isdir(target):
        os.mkdir(target)
    if len(files) == 0:
    	return jsonify(msg="FileNotFound")

    for file in files:
        name = Ids.get(Ids.id == 1).img
        filename = str(name) + file.filename[file.filename.index('.'):]
        destination = '/'.join([target, filename])
        file.save(destination)
        
    a = Ids.get(Ids.id == 1)
    a.img = int(a.img) + 1
    a.save()
    return filename