from flask import Blueprint, render_template, send_file

public_bp = Blueprint('public', __name__)

@public_bp.route("/")
def home(): return render_template('public/index.html')

@public_bp.route("/favicon.ico")
def favicon(): return send_file('static/favicon.svg')

