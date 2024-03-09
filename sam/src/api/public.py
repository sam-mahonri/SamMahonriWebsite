from ..database import Statistics, GeneralSettings
from ..admin.forms import GeneralSettingsForm
from ..enums import errors as Err
from ..enums import success as Ok
from .routes import api_bp, OUTPUT_TEMPLATE
from flask import jsonify
from bson import ObjectId

@api_bp.route('/general_settings/r/')
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