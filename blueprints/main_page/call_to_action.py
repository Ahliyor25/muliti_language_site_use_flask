
from flask import  jsonify, request
from flask import Blueprint
from flask_jwt_extended.view_decorators import jwt_required
from peewee import DoesNotExist
from models import CallToAction, Lang
import os

bp = Blueprint('cta',__name__, url_prefix = '/cta')

@bp.post('/')
@jwt_required()
def Create():
	
	_title = request.json.get('title')
	_des = request.json.get('des')
	_text_button = request.json.get('text_button')
	#_lang_id = request.json.get('lang_id')

	try:
		
		row = CallToAction(
		title = _title,
		des = _des,
		text_button = _text_button,
		#lang_id = _lang_id
		)
		row.save()

		return jsonify("done")
	except Exception as e:
		return '{}'.format(e)


@bp.get('/')
def Get():
	
	try:
		
		cta = CallToAction.select()
		
		js = []
	
		for i in cta:
			js.append({
				"id" : i.id,
				"title": i.title,
				"des" : i.des,
				"text_button": i.text_button,
				#"lang_id" : Lang.get(Lang.id == i.lang_id).title
			})
		return jsonify(js)
		
	except Exception as e:
		return '{}'.format(e)

@bp.put('/<id>')
@jwt_required()
def Update(id):
	
	try:
		cta = CallToAction.get(CallToAction.id == id)
	except DoesNotExist:
		return({"msg":"Не найден CallToAction по такому id"})
	try:
		cta.title  = request.json.get('title')
		cta.des  = request.json.get('des')
		cta.text_button  = request.json.get('') 
		#cta.lang_id = request.json.get('lang_id')
		cta.save()
		return  jsonify('done')
	except Exception as e:
			return '{}'.format(e)

@bp.delete('/<id>')
@jwt_required()
def Delete(id):
	try:
		cta = CallToAction.get(CallToAction.id == id)
	except DoesNotExist:
		return({"msg":"Не найден cta по такому id"})	
	try:
		cta.delete_instance()
		return jsonify({"msg" : "Done"})
	except Exception as e:
		return '{}'.format(e)