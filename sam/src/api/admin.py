from ..database import Statistics, GeneralSettings, Gallery
from ..admin.forms import GeneralSettingsForm, GalleryForm

from ..enums import errors as Err
from ..enums import success as Ok
from .routes import api_bp, OUTPUT_TEMPLATE
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity,
    set_access_cookies, unset_jwt_cookies, get_jwt
)
from flask import jsonify, request
from bson import ObjectId
from ..utils import upload_file


@api_bp.route('/general_settings/w/', methods=['POST', 'PUT'])
@jwt_required()
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
        
    return jsonify(result)

@api_bp.route('/gallery/list', methods=['GET'])
@jwt_required()
def list_gallery():
    result = OUTPUT_TEMPLATE
    try:
        page = int(request.args.get('page', 1))
        is_artwork = request.args.get('is_artwork')
        query = request.args.get('query')

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
    