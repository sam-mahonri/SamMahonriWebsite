from flask import Blueprint, render_template, send_file, session, request, redirect, flash, redirect, url_for, make_response
from flask_babel import gettext, lazy_gettext
from ..enums import errors as Err
from ..enums import success as Ok
from dotenv import load_dotenv
import os
from .forms import LoginForm
import requests
from ..database import User, Statistics, GeneralSettings, bcrypt
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity,
    set_access_cookies, unset_jwt_cookies, get_jwt
)
from ... import jwt, limiter
from datetime import timedelta, timezone, datetime
from ..utils.jwt_expiry import *
load_dotenv()

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route("/login", methods=['POST', 'GET'])
@limiter.limit("3 per minute")
def login():
    form = LoginForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data

            user = User.find_by_username(username)
            print(user)
            if user and bcrypt.check_password_hash(user['password'], password):
                user_identity = user['username']
                session['user'] = user_identity
                
                access_token = create_access_token(identity=user_identity, expires_delta=ACCESS_TOKEN_EXPIRY)
                resp = make_response(redirect(url_for('admin.admin')))
                
                set_access_cookies(resp, access_token)

                return resp
            else:
                flash(Err.Errors.INVALID_CREDENTIALS.value, 'error')
        else:
            flash(Err.Errors.ERROR_FORM.value, 'error')
    return render_template('admin/login.html', form=form)

@auth_bp.route("/logout")
def logout():
    resp = make_response(redirect(url_for('public.home')))
    unset_jwt_cookies(resp)
    if 'user' in session: session.pop('user')
    flash('Sessão de administrador encerrada', 'success')
    return resp