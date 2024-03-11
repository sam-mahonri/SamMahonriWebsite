from ..database import Statistics, GeneralSettings
from ..admin.forms import GeneralSettingsForm
from ..enums import errors as Err
from ..enums import success as Ok
from .routes import api_bp, OUTPUT_TEMPLATE
from flask import jsonify
from bson import ObjectId
