from flask import Blueprint, render_template, send_file, session, request, redirect, send_from_directory, current_app, url_for
from ..database import Statistics, GeneralSettings
public_bp = Blueprint('public', __name__)
import os
from ... import app
@public_bp.route("/lang/<lang>")
def lang(lang): 
    session["locale"] = lang
    page = request.args.get('page', '/')
    return redirect(page)

@public_bp.route("/")
def home(): 
    Statistics.update('accesses')
    return render_template('public/index.html')

@public_bp.route("/arts")
def arts(): 
    return render_template('public/gallery.html')

@public_bp.route("/commissions")
def comms(): 
    return render_template('public/commissions.html')

@public_bp.route("/favicon.ico")
def favicon(): return send_file('static/favicon.svg')

@public_bp.route("/gallery/image/<img>")
def get_image(img):
    path = current_app.config.get('UPLOAD_PATH', '/static/files')
    file_path = os.path.join(path, img)

    if os.path.exists(file_path):
        return send_from_directory(path, img)
    else:
        return send_from_directory(current_app.static_folder, 'favicon.svg')

@public_bp.app_context_processor
def inject_blueprint_variables():
    global_settings = GeneralSettings.find()
    if not global_settings: global_settings = {}
    return dict(global_settings=global_settings)