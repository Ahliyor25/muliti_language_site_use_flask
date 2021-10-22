
from flask import  jsonify, request
from flask import Blueprint
from peewee import DoesNotExist
from models import Lang
from utils import helper_var, upload_image
import os

bp = Blueprint('lang',__name__, url_prefix = '/lang')

host  = helper_var.host

@bp.post('/')
def CreateLang():
	
	_title  = request.form.get('title')
	_thumbnail = request.files.getlist('thumbnail')
	_slug = request.form.get('slug')
	_status = request.form.get('status')
	
	try:
		_thumbnail = upload_image(_thumbnail)
		row = Lang(
		title = _title, 
		thumbnail= _thumbnail,
		slug = _slug,
		status = _status)

		row.save()
		
		return jsonify("done")
	except Exception as e:
		return '{}'.format(e)

@bp.get('/')
def GetLang():
	
	try:
		lang = Lang.select()
		
		js = []
	
		for i in lang:
			js.append({
				"id" : i.id,
				"title": i.title,
				"slug": i.slug,
				"status" : i.status,
				"thumbnail" : host + i.thumbnail,
			})
		return jsonify(js)
		
	except Exception as e:
		return '{}'.format(e)

@bp.put('/<id>')
def UpdateLang(id):
	
	try:
		lang = Lang.get(Lang.id == id)
	except DoesNotExist:
		return({"msg":"Не найден проект по такому id"})

	try:
		
		lang.title  = request.form.get('title')
		lang.slug = request.form.get('slug')
		lang.status = request.form.get('status')
		thumbnail = request.files.getlist('thumbnail')
		
	
	
		if len(thumbnail) == 0:
			lang.save()
			response = jsonify('done1')
			return response
		os.remove(helper_var.path + 'images/' + lang.thumbnail)
		_thumbnail = upload_image(thumbnail)
	
		lang.thumbnail = _thumbnail
		lang.save()
		
		  
		
		response = jsonify('done')
		return response
	except Exception as e:
			return '{}'.format(e)



@bp.delete('/<id>')
def DeleteLang(id):
	try:
		a = Lang.get(Lang.id == id)
	except DoesNotExist:
		return({"msg":"Не найден проект по такому id"})	
	try:
		img_path = helper_var.path+'images/'+a.thumbnail
		os.remove(img_path)
		a.delete_instance()
		return jsonify({"msg" : "Done"})
	except Exception as e:
		return '{}'.format(e)