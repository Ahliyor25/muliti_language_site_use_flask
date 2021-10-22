from utils import hash_string_sha256
from flask import  jsonify, request
from flask_jwt_extended import (
	JWTManager, jwt_required, create_access_token,
	get_jwt_identity, decode_token
)
from flask import Blueprint
from flask_cors import cross_origin
from models import *
from peewee import *

bp = Blueprint('login',__name__,url_prefix = '/login')

@bp.post('/')
@cross_origin()
def LogIn():
	try:
		_username = request.json.get('username')
		_password = request.json.get('password')
		
		query = User.select().where((User.username == _username))
		if not query.exists():
			return jsonify({"msg": "DoesNotExists"})
		for i in query:
			if i.password == hash_string_sha256(_password):
				access_token = create_access_token(identity=i.username)
				response = jsonify({"id": i.id,
				"username": i.username,
				"password" : i.password,
				"access_token" : access_token })
				return response
			else: return ({"msg":"Не правильный пароль"})
	except Exception as e:
		return '{}'.format(e)


@bp.post('/signup')
@cross_origin()
def SignUp():
	try:
	#id username password name email phone
		_username = request.json.get('username')
		_password = request.json.get('password')
		access_token = create_access_token(identity=_username)
		us = User( username = _username, password = hash_string_sha256(_password))
		us.save()
		return jsonify(access_token=access_token), 200
	except Exception as e:
		return '{}'.format(e)



			


@bp.put('/user/<id>')
@jwt_required()
@cross_origin()
def UpdateUser(id):
	
	try:
		usr = User.get(User.id == id)
	except DoesNotExist:
		return({"msg":"Не найден User по такому id"})
	
	try:
		usr.username  = request.json.get('username')
		usr.password =  request.json.get('password')
	

		usr.save()
		response = jsonify('done')
		return response
	except Exception as e:
			return '{}'.format(e)
			
@bp.get('/user')
@jwt_required()
def GetUser():
	try:
		p = request.args.get('page',1)
		prj = User.select().order_by(User.id).paginate(int(p),6)
		count = User.select().count()
		js = {"count" : 0, 'users' : []}
		if count%6==0:
			js['count'] = count//6
		elif count > 6:
			js['count'] = count //6 + 1
		else:
			js['count'] = 1
		for i in prj:
			js['users'].append({
				"id" : i.id,
			
				"username" : i.username,
				"password" : i.password
			})
		return jsonify(js)
	except Exception as e:
			return '{}'.format(e)
			
@bp.delete('/user/<id>')
@jwt_required()
@cross_origin()
def UsersDelete(id):
	try:
		a = User.get(User.id == id)
	except DoesNotExist:
		return({"msg":"Не найден Users  по такому id"})	
	try:
		a.delete_instance()
		return jsonify({"msg" : "Done"})
	except Exception as e:
		return '{}'.format(e)