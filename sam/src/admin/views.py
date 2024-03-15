from flask import Blueprint, render_template, send_file, session, request, redirect, flash, redirect, url_for, make_response, json
from flask_babel import gettext, lazy_gettext
from ..enums import errors as Err
from ..enums import success as Ok
from dotenv import load_dotenv
import os
from .forms import GeneralSettingsForm
import requests
from ..database import User, Statistics, GeneralSettings, bcrypt
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity,
    set_access_cookies, unset_jwt_cookies, get_jwt
)
from ... import jwt, limiter
from ..api.routes import general_settings_w, general_settings_r
from ..auth import refresh_expiring_jwts

from datetime import timedelta, timezone, datetime
from ..utils.jwt_expiry import *
from ..utils.view_helper import *
load_dotenv()

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.after_request
def refresh_token(response):
    return refresh_expiring_jwts(response)

@admin_bp.route("/", methods=['POST', 'GET'])
@jwt_required()
def admin(only_data = False): 
    Statistics.reset_weekly()
    statistics = Statistics.find()
    form = GeneralSettingsForm()
    
    data = (lambda r: r.json if r.status_code == 200 else None)(general_settings_r())
    current_global_settings = data.get("data", None)
    
    if request.method == "POST":
        data = (lambda r: r.json if r.status_code == 200 else None)(general_settings_w())
        launch_flash_response(data)
        form = form_errors_normalize_response(form, data)
    else: form = form_data_normalize(form, current_global_settings)
    
    if not only_data: return render_template('admin/index.html', statistics=statistics, form = form)
    else: return statistics, form


@admin_bp.route("/gallery", methods=['POST', 'GET'])
@jwt_required()
def gallery(): return render_template('admin/gallery.html')
