from flask import Blueprint, render_template, send_file, session, request, redirect
from ..database import Statistics
public_bp = Blueprint('public', __name__)

@public_bp.route("/lang/<lang>")
def lang(lang): 
    session["locale"] = lang
    page = request.args.get('page', '/')
    return redirect(page)

@public_bp.route("/")
def home(): 
    Statistics.update('accesses')
    return render_template('public/index.html')

@public_bp.route("/favicon.ico")
def favicon(): return send_file('static/favicon.svg')

