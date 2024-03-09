from flask import Blueprint, render_template, send_file, session, request, redirect, flash, redirect, url_for, make_response
from flask_babel import gettext, lazy_gettext
from ..enums import errors as Err
from ..enums import success as Ok
from dotenv import load_dotenv
import os
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

api_bp = Blueprint('api', __name__, url_prefix='/api')

OUTPUT_TEMPLATE = {
        "success":False,
        "message":Err.Errors.GENERIC_ERROR.value,
        "data":None
    }