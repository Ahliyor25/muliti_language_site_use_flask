import os
from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required
from models import Residence
from peewee import *
from utils import helper_var, upload_image


bp = Blueprint('residence', __name__, url_prefix='/residence')

@bp.post('/')
@jwt_required()
def create_residence():
    data = request.form.get
    img = request.files.getlist('img')

    if request.files['img'].filename == '':
	    return jsonify({'message':'No file [img] selected'}),400
    else:
        _img = upload_image(img)
    
    Residence.create(
        name=data('name'),
        img = _img)
    return jsonify({'message':'Residence created'}),201


@bp.get('/')
def get_residences():
        p = request.args.get('page',1)
        residences = Residence.select().order_by(Residence.id).paginate(int(p),6) 
        count = Residence.select().count()
        js = {"count" : 0, 'residence' : []}
        if count%6==0:
            js['count'] = count//6
        elif count>6:
            js['count'] = count//6+1
        else:
            js['count'] = 1
        for residence in residences:
            js['residence'].append(
                {
                    'id':residence.id,
                    'name':residence.name,
                    'img':helper_var.host + residence.img
                }
                )
        return jsonify(js),200

@bp.put('/<id>')
@jwt_required()
def update_residence(id):
    try:
        residence = Residence.get_by_id(id)
    except Residence.DoesNotExist:
        return jsonify({'message':'Residence not found'}),404
    
    data = request.form.get
    img = request.files.getlist('img')
    if request.files['img'].filename == '':
        residence.name = data('name')
        residence.save()
        return jsonify({'message':'Residence updated'}),200
    else:
        img_path = helper_var.path+'images/'+ residence.img
        os.remove(img_path)
        _img = upload_image(img)
       
        residence.name = data('name')
        residence.img = _img
        residence.save()
        return jsonify({'message':'Residence updated'}),200


@bp.delete('/<id>')
@jwt_required()
def delete_residence(id):
    try:
        residence = Residence.get_by_id(id)
    except Residence.DoesNotExist:
        return jsonify({'message':'Residence not found'}),404
    img_path = helper_var.path+'images/'+ residence.img
    os.remove(img_path)
    residence.delete_instance()
    return jsonify({'message':'Residence deleted'}),200