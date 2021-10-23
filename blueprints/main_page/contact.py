
from flask import  jsonify, request
from flask import Blueprint
from flask_jwt_extended.view_decorators import jwt_required
from peewee import DoesNotExist
from models import Contact, Lang
import os

bp = Blueprint('contact',__name__, url_prefix = '/contact')

@bp.post('/')
@jwt_required()
def Create():
	
	_title = request.json.get('title')
	_des = request.json.get('des')
	_address = request.json.get('address')
	_phone = request.json.get('phone')
	_email = request.json.get('email')
	_text_button = request.json.get('text_button')
	_longitude = request.json.get('longitude')
	_latitude = request.json.get('latitude')
	_lang_id = request.json.get('lang_id')

	try:
		
		row = Contact(
		title = _title,
		des = _des,
		address = _address,
		phone = _phone,
		email = _email,
		text_button = _text_button,
		longitude = _longitude,
		latitude = _latitude,
		lang_id = _lang_id
		)
		row.save()

		return jsonify("done")
	except Exception as e:
		return '{}'.format(e)


@bp.get('/')
def Get():
	
	try:

		contact = Contact.select()
		
		js = []
	
		for i in contact:
			js.append({
				"id" : i.id,
				"title": i.title,
				"des" : i.des,
				"address": i.address,
				"phone": i.phone,
				"email": i.email,
				"text_button": i.text_button,
				"longitude": i.longitude,
				"latitude": i.latitude,
				"lang_id" : Lang.get(Lang.id == i.lang_id).title
			})
		return jsonify(js)
		
	except Exception as e:
		return '{}'.format(e)

@bp.put('/<id>')
@jwt_required()
def Update(id):
	
	try:
		contact = Contact.get(Contact.id == id)
	except DoesNotExist:
		return({"msg":"Не найден CallToAction по такому id"})
	try:
		contact.title  = request.json.get('title')
		contact.des  = request.json.get('des')
		contact.address  = request.json.get('address')
		contact.phone  = request.json.get('phone')
		contact.email  = request.json.get('email')
		contact.text_button  = request.json.get('text_button') 
		contact.longitude  = request.json.get('longitude')
		contact.latitude  = request.json.get('latitude')
		contact.lang_id = request.json.get('lang_id')
		contact.save()
		return  jsonify('done')
	except Exception as e:
			return '{}'.format(e)

@bp.delete('/<id>')
@jwt_required()
def Delete(id):
	try:
		contact = Contact.get(Contact.id == id)
	except DoesNotExist:
		return({"msg":"Не найден cta по такому id"})	
	try:
		contact.delete_instance()
		return jsonify({"msg" : "Done"})
	except Exception as e:
		return '{}'.format(e)