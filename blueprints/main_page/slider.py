
from flask import  jsonify, request
from flask import Blueprint
from flask_jwt_extended.view_decorators import jwt_required
from peewee import DoesNotExist
from models import Lang, Slider
from utils import helper_var, upload_image
import os

bp = Blueprint('slider',__name__, url_prefix = '/slider')

host  = helper_var.host

@bp.post('/')
@jwt_required()
def CreateSlider():
	
	_name = request.form.get('name')
	img = request.files.getlist('img')
	#_lang_id = request.form.get('lang_id')
	
	try:
		_img = upload_image(img)

		row = Slider(
		name = _name,
		img = _img,
		#lang_id = _lang_id
		)

		row.save()
		
		return jsonify("done")
	except Exception as e:
		return '{}'.format(e)

@bp.get('/')
def GetSlider():
	
	try:
		slider = Slider.select()
		
		js = []
	
		for i in slider:
			js.append({
				"id" : i.id,
				"name": i.name,
				"img": host + i.img,
				#"lang_id" : Lang.get(Lang.id == i.lang_id).title
			})
		return jsonify(js)
		
	except Exception as e:
		return '{}'.format(e)

@bp.put('/<id>')
def UpdateSlider(id):
	
	try:
		slider = Slider.get(Slider.id == id)
	except DoesNotExist:
		return({"msg":"Не найден Слайдер по такому id"})

	try:
		
		slider.name  = request.form.get('name')
		img =   request.files.getlist('img')
		#slider.lang_id = request.form.get('lang_id')
		
	
		if len(img) == 0:
			slider.save()
			return jsonify('done')
		
		_img = upload_image(img)
	
		slider.img = _img
		slider.save()
	
		response = jsonify('done')
		return response
	except Exception as e:
			return '{}'.format(e)



@bp.delete('/<id>')
def DeleteSlider(id):
	try:
		slider = Slider.get(Slider.id == id)
	except DoesNotExist:
		return({"msg":"Не найден проект по такому id"})	
	try:
		img_path = helper_var.path+'images/'+slider.img
		if slider.img is not  None:
			os.remove(img_path)
		slider.delete_instance()
		return jsonify({"msg" : "Done"})
	except Exception as e:
		return '{}'.format(e)