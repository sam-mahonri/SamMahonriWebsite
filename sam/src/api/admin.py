from ..database import Statistics, GeneralSettings
from ..admin.forms import GeneralSettingsForm
from ..enums import errors as Err
from ..enums import success as Ok
from .routes import api_bp, OUTPUT_TEMPLATE
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity,
    set_access_cookies, unset_jwt_cookies, get_jwt
)
from flask import jsonify

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
    
    result["data"] = {"form_data": form.data, "form_errors": form.errors}
    
    return jsonify(result)

