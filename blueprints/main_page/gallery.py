
from flask import  jsonify, request
from flask import Blueprint
from flask_jwt_extended.view_decorators import jwt_required
from peewee import DoesNotExist
from models import Gallery
from utils import helper_var, upload_image
import os

bp = Blueprint('gallery',__name__, url_prefix = '/gallery')

host  = helper_var.host

@bp.post('/')
@jwt_required()
def Create():

	img = request.files.getlist('img')
	try:
		_img = upload_image(img)
		row = Gallery(
		img = _img,
		)
		row.save()
		return jsonify("done")
	except Exception as e:
		return '{}'.format(e)

@bp.get('/')
def Get():
	
	try:
		
		g = Gallery.select()
		
		js = []
	
		for i in g:
			js.append({
				"id" : i.id,
				"img": host + i.img,
			})
		return jsonify(js)
		
	except Exception as e:
		return '{}'.format(e)

@bp.put('/<id>')
@jwt_required()
def Update(id):
	
	try:
		g = Gallery.get(Gallery.id == id)
	except DoesNotExist:
		return({"msg":"Не найден Галерея по такому id"})
	try:
		img =   request.files.getlist('img')
	
		if len(img) == 0:
			g.save()
			return jsonify('done')
		os.remove(helper_var.path + 'images/' + g.img)
		_img = upload_image(img)
	
		g.img = _img
		g.save()
	
		response = jsonify('done')
		return response
	except Exception as e:
			return '{}'.format(e)



@bp.delete('/<id>')
@jwt_required()
def Delete(id):
	try:
		g = Gallery.get(Gallery.id == id)
	except DoesNotExist:
		return({"msg":"Не найден Gallery по такому id"})	
	try:
		img_path = helper_var.path+'images/'+ g.img
		if g.img is not  None:
			os.remove(img_path)
		g.delete_instance()
		return jsonify({"msg" : "Done"})
	except Exception as e:
		return '{}'.format(e)