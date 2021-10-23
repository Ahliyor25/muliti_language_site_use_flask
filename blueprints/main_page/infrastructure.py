
from flask import  jsonify, request
from flask import Blueprint
from flask_jwt_extended.view_decorators import jwt_required
from peewee import DoesNotExist
from models import Infrastructure, Lang
from utils import helper_var, upload_image
import os

bp = Blueprint('infrastructure',__name__, url_prefix = '/infrastructure')

host  = helper_var.host

@bp.post('/')
@jwt_required()
def Create():
	
	img = request.files.getlist('img')

	_title = request.form.get('title')
	_des = request.form.get('des')
	
	_lang_id = request.form.get('lang_id')

	try:
		
		_img = upload_image(img)
		row = Infrastructure(
		title = _title,
		img = _img,
		des = _des,
		lang_id = _lang_id
		)

		row.save()
	
		return jsonify("done")
	except Exception as e:
		return '{}'.format(e)

@bp.get('/')
def Get():
	
	try:
		
		infra = Infrastructure.select()
		
		js = []
	
		for i in infra:
			js.append({
				"id" : i.id,
				"title": i.title,
				"img": host + i.img,
				"des" : i.des,
				"lang_id" : Lang.get(Lang.id == i.lang_id).title
			})
		return jsonify(js)
		
	except Exception as e:
		return '{}'.format(e)

@bp.put('/<id>')
@jwt_required()
def Update(id):
	
	try:
		infra = Infrastructure.get(Infrastructure.id == id)
	except DoesNotExist:
		return({"msg":"Не найден Слайдер по такому id"})
	try:
		
		infra.title  = request.form.get('title')
		img =   request.files.getlist('img')
		infra.des  = request.form.get('des')
		infra.lang_id = request.form.get('lang_id')
		
	
		if len(img) == 0:
			infra.save()
			return jsonify('done')
		os.remove(helper_var.path + 'images/' + infra.img)	
		
		_img = upload_image(img)
	
		infra.img = _img
		infra.save()
	
		response = jsonify('done')
		return response
	except Exception as e:
			return '{}'.format(e)



@bp.delete('/<id>')
@jwt_required()
def Delete(id):
	try:
		infra = Infrastructure.get(Infrastructure.id == id)
	except DoesNotExist:
		return({"msg":"Не найден проект по такому id"})	
	try:
		img_path = helper_var.path+'images/'+ infra.img
		if infra.img is not  None:
			os.remove(img_path)
		infra.delete_instance()
		return jsonify({"msg" : "Done"})
	except Exception as e:
		return '{}'.format(e)