"""
Main file
Connects all blueprint
Add Cors policy
"""

from flask import Flask, send_file
from flask_cors import CORS
from utils import (
  register_blueprints_login,
  register_blueprints_main_page
)
from flask_jwt_extended import JWTManager
from datetime import timedelta





app = Flask(__name__)

app.secret_key = 'LPOI(U*((IU*&T^YHJKOL:>:<LjidnkjiuwefjiTFRDES).<mjhuio'
CORS(app)
jwt = JWTManager(app)
app.jwt_secret_key = 'aoaoaoaoaoaoaooaaooaoaoaoa'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=48)

register_blueprints_login(app)
register_blueprints_main_page(app)


@app.route('/getimg/<name>')

def GetImg(name):
	return send_file('images/'+name)
