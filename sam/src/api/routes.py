from flask import Blueprint, render_template, send_file, session, request, redirect, flash, redirect, url_for, make_response, jsonify
from flask_babel import gettext, lazy_gettext
from ..enums import errors as Err
from ..enums import success as Ok
from dotenv import load_dotenv
import os
import requests
from ..database import User, Statistics, GeneralSettings, Gallery, Modalities, bcrypt
from ..admin.forms import GeneralSettingsForm, GalleryForm, GalleryEditForm, DeleteItem, BaseCommissionType, EditCommissionType
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity,
    set_access_cookies, unset_jwt_cookies, get_jwt
)
from ... import jwt, limiter
from datetime import timedelta, timezone, datetime
from ..utils.jwt_expiry import *
from bson import ObjectId
from ..utils import upload_file
load_dotenv()

api_bp = Blueprint('api', __name__, url_prefix='/api')

OUTPUT_TEMPLATE = {
        "success":False,
        "message":Err.Errors.GENERIC_ERROR.value,
        "data":None
    }

@api_bp.route('/general_settings/w/', methods=['POST', 'PUT'])
@jwt_required()
@limiter.limit("1/second")
def general_settings_w():
    result = OUTPUT_TEMPLATE
    
    form = GeneralSettingsForm()
    if form.validate_on_submit():
        data = form.data
        data.pop('csrf_token')
        if GeneralSettings.update(data):
            result = {"success": True, "message": Ok.Success.SUCCESS_SAVED.value}
        else: result = {"success": False, "message": Err.Errors.ERROR_GET_DATA.value}
    else: result = {"success": False, "message": Err.Errors.ERROR_FORM.value}
    
    result["data"] = {"form_fields": form.data, "form_errors": form.errors}
    
    return jsonify(result)

@api_bp.route('/general_settings/r/')
@jwt_required()
def general_settings_r():
    result = OUTPUT_TEMPLATE
    
    current_global_settings = GeneralSettings.find()
    if current_global_settings: 
        for key, value in current_global_settings.items():
            if isinstance(value, ObjectId):
                current_global_settings[key] = str(value)
        result = {"success": True, "message":"", "data":current_global_settings}
    else: result = {"success": False, "message":""}
    
    return jsonify(result)

@api_bp.route('/gallery/image', methods=['POST', 'PUT', 'DELETE'])
@jwt_required()
@limiter.limit("1/second")
def upload_image():
    result = OUTPUT_TEMPLATE
    
    if request.method == "POST":
        
        form = GalleryForm()
        warn = {}
        image_id = None
        
        if form.validate_on_submit():
            file = form.image.data
            warn = upload_file.save_image(file, ignore_original=True)
            
            if warn.get('success', False): 
                image_id = Gallery.create(form.title.data, warn.get("url"), warn.get("compressed_path"), warn.get("resized_path"), form.redirect_link.data, form.is_artwork.data)
                if image_id:
                    if form.is_artwork.data: Statistics.update('arts')
                    result = {"success": True, "message": Ok.Success.SUCCESS_UPLOAD.value}
                else:
                    result = {"success": False, "message": Err.Errors.DB_SAVE_PROBLEM.value}
            else: result = {"success": False, "message": warn.get('message', Err.Errors.FILE_PROBLEM.value)}
        else: 
            
            result = {"success": False, "message": Err.Errors.ERROR_FORM.value}
        
        form.image.data = {}
        warn["bd_img_id"] = image_id
        result["data"] = {"form_fields": form.data, "form_errors": form.errors, "image_data": warn}
    
    elif request.method == "PUT":
        form = GalleryEditForm()
        if form.validate_on_submit():
            result["success"] = Gallery.update(form.image_id.data, form.title.data, None, None, None, form.redirect_link.data, form.is_artwork.data)
            result["message"] = Ok.Success.SUCCESS_SAVED.value if result["success"] else Err.Errors.NO_CHANGES.value
        else: 
            result = {"success": False, "message": Err.Errors.ERROR_FORM.value}
            
        result["data"] = {"form_fields": form.data, "form_errors": form.errors}
        
    elif request.method == "DELETE":
        form = DeleteItem()
        if form.validate_on_submit():
            if form.please_delete.data:
                result["success"] = Gallery.delete(form.item_id.data)
                result["message"] = Ok.Success.SUCCESS_DELETED.value if result["success"] else Err.Errors.NO_CHANGES.value
            else:
                result["success"] = False
                result["message"] = Err.Errors.NO_CHANGES.value
        else: 
            result = {"success": False, "message": Err.Errors.ERROR_FORM.value}
        
        result["data"] = {"form_fields": form.data, "form_errors": form.errors}
        
    return jsonify(result)

@api_bp.route('/commissions/modality', methods=['POST', 'PUT', 'DELETE'])
@jwt_required()
def modalities():
    result = OUTPUT_TEMPLATE
    
    if request.method == "POST":
        form = BaseCommissionType()
        slug = None
        if form.validate_on_submit():
            data = form.data
            data.pop('csrf_token')
            slug = Modalities.create(data=data)
            result["success"] = True if slug else False
            result["message"] = Ok.Success.SUCCESS_POST.value if slug else Err.Errors.DB_SAVE_PROBLEM.value
        else: 
            result = {"success": False, "message": Err.Errors.ERROR_FORM.value}
        result["data"] = {"form_fields": form.data, "form_errors": form.errors, "slug": slug if slug else ''}
        
    elif request.method == "PUT":
        form = EditCommissionType()
        if form.validate_on_submit():
            data = form.data
            data.pop('csrf_token')
            result["success"] = Modalities.update_by_slug(slug = data.get("slug"), data = data) 
            result["message"] = Ok.Success.SUCCESS_SAVED.value if result["success"] else Err.Errors.NO_CHANGES.value
        else: 
            result = {"success": False, "message": Err.Errors.ERROR_FORM.value}
        result["data"] = {"form_fields": form.data, "form_errors": form.errors}
        
    elif request.method == "DELETE":
        form = DeleteItem()
        if form.validate_on_submit():
            if form.please_delete.data:
                result["success"] = Modalities.delete_by_slug(form.item_id.data)
                result["message"] = Ok.Success.SUCCESS_DELETED.value if result["success"] else Err.Errors.NO_CHANGES.value
            else:
                result["success"] = False
                result["message"] = Err.Errors.NO_CHANGES.value
        else: 
            result = {"success": False, "message": Err.Errors.ERROR_FORM.value}
        result["data"] = {"form_fields": form.data, "form_errors": form.errors}
    
    return jsonify(result)

@api_bp.route('/commissions/modality/list', methods=['GET'])
def list_modalities():
    result = OUTPUT_TEMPLATE
    try:
        page = int(request.args.get('page', 1))
        tag = request.args.get('tag', None)
        query = request.args.get('query', None)

        modalities, _total_pages = Modalities.list_all(page=page, query=None)

        if modalities:
            result = {
                "success": True,
                "message": Ok.Success.SUCCESS_LOADED.value,
                "data": {
                    "modalities": modalities,
                    "_total_pages": _total_pages
                }
            }
        else:
            result = {
                "success": False,
                "message": Err.Errors.NOT_FOUND.value
            }
    except Exception as e:
        print(f"Erro ao listar imagens: {str(e)}")
        result = {
            "success": False,
            "message": Err.Errors.GENERIC_ERROR.value
        }

    return jsonify(result)

@api_bp.route('/gallery/list', methods=['GET'])
def list_gallery():
    result = OUTPUT_TEMPLATE
    try:
        page = int(request.args.get('page', 1))
        is_artwork = request.args.get('is_artwork', None)
        query = request.args.get('query', None)

        images = Gallery.find(page=page, is_artwork=is_artwork, title=query)

        if images:
            result = {
                "success": True,
                "message": Ok.Success.SUCCESS_LOADED.value,
                "data": {
                    "images": images
                }
            }
        else:
            result = {
                "success": False,
                "message": Err.Errors.NO_IMAGES_FOUND.value
            }
    except Exception as e:
        print(f"Erro ao listar imagens: {str(e)}")
        result = {
            "success": False,
            "message": Err.Errors.GENERIC_ERROR.value
        }

    return jsonify(result)