
from flask import  jsonify, request
from flask import Blueprint
from flask_jwt_extended.view_decorators import jwt_required
from peewee import DoesNotExist
from models import SectionThree, Lang, SectionThree, Slider
from utils import helper_var, upload_image
import os

bp = Blueprint('section_three',__name__, url_prefix = '/section_three')

host  = helper_var.host

@bp.post('/')
@jwt_required()
def CreateSectionThree():
	
	
	img = request.files.getlist('img')
	_title = request.form.get('title')
	_des = request.form.get('des')
	#_lang_id = request.form.get('lang_id')
	
	try:
		_img = upload_image(img)

		row = SectionThree(title = _title, img = _img, des = _des,
		 #lang_id = _lang_id,
		 )

		row.save()
	
		return jsonify("done")
	except Exception as e:
		return '{}'.format(e)

@bp.get('/')
def GetAdvantage():
	
	try:
		sectionThree = SectionThree.select()
		
		js = []
	
		for i in sectionThree:
			js.append({
				"id" : i.id,
				"title": i.title,
				"img": host + i.img,
				"des" : i.des,
				#"lang_id" : Lang.get(Lang.id == i.lang_id).title
			})
		return jsonify(js)
		
	except Exception as e:
		return '{}'.format(e)

@bp.put('/<id>')
@jwt_required()
def UpSectionThree(id):
	
	try:
		sectionThree = SectionThree.get(SectionThree.id == id)
	except DoesNotExist:
		return({"msg":"Не найден Слайдер по такому id"})
	try:
		
		sectionThree.title  = request.form.get('title')
		img =   request.files.getlist('img')
		SectionThree.des  = request.form.get('des')
		SectionThree.lang_id = request.form.get('lang_id')
		
	
		if len(img) == 0:
			sectionThree.save()
			return jsonify('done')
		
		_img = upload_image(img)
	
		sectionThree.img = _img
		sectionThree.save()
	
		response = jsonify('done')
		return response
	except Exception as e:
			return '{}'.format(e)



@bp.delete('/<id>')
@jwt_required()
def DeleteUpSectionThree(id):
	try:
		sectionThree = SectionThree.get(SectionThree.id == id)
	except DoesNotExist:
		return({"msg":"Не найден проект по такому id"})	
	try:
		img_path = helper_var.path+'images/'+ sectionThree.img
		if sectionThree.img is not  None:
			os.remove(img_path)
		sectionThree.delete_instance()
		return jsonify({"msg" : "Done"})
	except Exception as e:
		return '{}'.format(e)