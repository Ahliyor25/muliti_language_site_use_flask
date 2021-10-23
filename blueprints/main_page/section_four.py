
from flask import  jsonify, request
from flask import Blueprint
from flask_jwt_extended.view_decorators import jwt_required
from peewee import DoesNotExist
from models import Lang, SectionFour
from utils import helper_var, upload_image
import os

bp = Blueprint('section_four',__name__, url_prefix = '/section_four')

host  = helper_var.host

@bp.post('/')
@jwt_required()
def CreateSectionFour():
	
	img = request.files.getlist('img')

	_title = request.form.get('title')
	_des = request.form.get('des')
	_youtube_button_text = request.form.get('youtube_button_text')
	_text_advantage = request.form.get('text_advantage')
	_text_button = request.form.get('text_button')
	_lang_id = request.form.get('lang_id')

	try:
		
		_img = upload_image(img)
		row = SectionFour(
		title = _title,
		img = _img,
		des = _des,
		youtube_button_text = _youtube_button_text,
		text_advantage = _text_advantage,
		text_button = _text_button,
		lang_id = _lang_id
		)

		row.save()
	
		return jsonify("done")
	except Exception as e:
		return '{}'.format(e)

@bp.get('/')
def GetSectionFour():
	
	try:
		sectionFour = SectionFour.select()
		
		js = []
	
		for i in sectionFour:
			js.append({
				"id" : i.id,
				"title": i.title,
				"img": host + i.img,
				"des" : i.des,
				"youtube_button_text" : i.youtube_button_text,
				"text_advantage" : i.text_advantage,
				"text_button" : i.text_button,
				"lang_id" : Lang.get(Lang.id == i.lang_id).title
			})
		return jsonify(js)
		
	except Exception as e:
		return '{}'.format(e)

@bp.put('/<id>')
@jwt_required()
def UpSectionFour(id):
	
	try:
		sectionFour = SectionFour.get(SectionFour.id == id)
	except DoesNotExist:
		return({"msg":"Не найден Слайдер по такому id"})
	try:
		
		sectionFour.title  = request.form.get('title')
		img =   request.files.getlist('img')
		sectionFour.des  = request.form.get('des')
		sectionFour.lang_id = request.form.get('lang_id')
		sectionFour.youtube_button_text = request.form.get('youtube_button_text')
		sectionFour.text_advantage = request.form.get('text_advantage')
		sectionFour.text_button = request.form.get('text_button')
		
	
		if len(img) == 0:
			sectionFour.save()
			return jsonify('done')
		
		_img = upload_image(img)
	
		sectionFour.img = _img
		sectionFour.save()
	
		response = jsonify('done')
		return response
	except Exception as e:
			return '{}'.format(e)



@bp.delete('/<id>')
@jwt_required()
def DeleteUpSectionFour(id):
	try:
		sectionFour = SectionFour.get(SectionFour.id == id)
	except DoesNotExist:
		return({"msg":"Не найден проект по такому id"})	
	try:
		img_path = helper_var.path+'images/'+ sectionFour.img
		if sectionFour.img is not  None:
			os.remove(img_path)
		sectionFour.delete_instance()
		return jsonify({"msg" : "Done"})
	except Exception as e:
		return '{}'.format(e)