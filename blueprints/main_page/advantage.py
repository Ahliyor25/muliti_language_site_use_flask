
from flask import  jsonify, request
from flask import Blueprint
from flask_jwt_extended.view_decorators import jwt_required
from peewee import DoesNotExist
from models import Advantage, Lang, Slider
from utils import helper_var, upload_image
import os

bp = Blueprint('advantage',__name__, url_prefix = '/advantage')

host  = helper_var.host

@bp.post('/')
@jwt_required()
def CreateAdvantage():
	
	_title = request.form.get('title')
	icon = request.files.getlist('icon')
	_des = request.form.get('des')
	_lang_id = request.form.get('lang_id')
	
	try:
		_icon = upload_image(icon)

		row = Advantage(title = _title, icon = _icon, des = _des, lang_id = _lang_id)

		row.save()
	
		return jsonify("done")
	except Exception as e:
		return '{}'.format(e)

@bp.get('/')
def GetAdvantage():
	
	try:
		advantage = Advantage.select()
		
		js = []
	
		for i in advantage:
			js.append({
				"id" : i.id,
				"title": i.title,
				"icon": host + i.icon,
				"des" : i.des,
				"lang_id" : Lang.get(Lang.id == i.lang_id).title
			})
		return jsonify(js)
		
	except Exception as e:
		return '{}'.format(e)

@bp.put('/<id>')
def UpAdvantage(id):
	
	try:
		advantage = Advantage.get(Advantage.id == id)
	except DoesNotExist:
		return({"msg":"Не найден Слайдер по такому id"})

	try:
		
		advantage.title  = request.form.get('name')
		icon =   request.files.getlist('icon')
		advantage.des  = request.form.get('des')
		advantage.lang_id = request.form.get('lang_id')
		
	
		if len(icon) == 0:
			advantage.save()
			return jsonify('done')
		
		_icon = upload_image(icon)
	
		advantage.icon = _icon
		advantage.save()
	
		response = jsonify('done')
		return response
	except Exception as e:
			return '{}'.format(e)



@bp.delete('/<id>')
def DeleteSlider(id):
	try:
		advantage = Advantage.get(Advantage.id == id)
	except DoesNotExist:
		return({"msg":"Не найден проект по такому id"})	
	try:
		img_path = helper_var.path+'images/'+ advantage.icon
		if advantage.icon is not  None:
			os.remove(img_path)
		advantage.delete_instance()
		return jsonify({"msg" : "Done"})
	except Exception as e:
		return '{}'.format(e)