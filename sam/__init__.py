from flask import Flask, request, session, render_template, flash, make_response, jsonify
from config import Config
from flask_cors import CORS
from flask_babel import Babel, _
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_limiter import Limiter
from pymongo import MongoClient
from flask_jwt_extended import JWTManager, exceptions
from flask_wtf.csrf import CSRFProtect
from .src.enums import errors as Err
from .src.utils import aproximate

app = Flask(__name__)

from dotenv import load_dotenv
import os
load_dotenv()

app.config.from_object(Config)

limiter = Limiter(
    key_func=Config.LIMITER_KEY_FUNC,
    storage_uri=Config.LIMITER_STORAGE_URI,
    app=app,
    default_limits=["256 per minute", "50 per second"]
    )

CORS(app)
csrf = CSRFProtect(app)
jwt = JWTManager(app)
mongo_client = MongoClient(app.config["MONGO_URI"])

def get_locale():
    locale_session = session.get("locale", None)
    
    if locale_session is None: locale_session = request.accept_languages.best_match(app.config['LANGUAGES'])
    if not locale_session in app.config.get('LANGUAGES'): 
        flash(Err.Errors.INVALID_LANGUAGE.value)
        locale_session = app.config.get('BABEL_DEFAULT_LOCALE')
        session["locale"] = locale_session
    
    return locale_session

babel = Babel(app, locale_selector = get_locale)

@app.context_processor
def inject_in_template():
    return dict(current_language = get_locale())

app.jinja_env.globals.update(format_relative_time=aproximate.format_relative_time)

@app.errorhandler(Exception)
def handle_error(error):
    print(error)
    status_code = getattr(error, 'code', 500)
    return render_template('layouts/errorpage.html', error=error, status_code=status_code), status_code

@jwt.expired_token_loader
def expired_token_callback(expired_token, callback):
    if 'user' in session: session.pop('user')
    flash(Err.Errors.TOKEN_EXPIRED.value, "error")
    return make_response(render_template("layouts/errorpage.html", error=Err.Errors.SESSION_EXPIRED.value, status_code=401), 401)

@jwt.unauthorized_loader
def unauthorized_callback(callback):
    if 'user' in session: session.pop('user')
    flash(Err.Errors.UNAUTHORIZED_ACCESS.value, "error")
    return make_response(render_template("layouts/errorpage.html", error=str(callback), status_code=401), 401)

def create_app():
    jwt.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)
    
    from .src.public.views import public_bp
    from .src.admin.views import admin_bp
    from .src.auth.views import auth_bp
    from .src.api.routes import api_bp
    from .src.macro.views import macro_bp
    
    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(macro_bp)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)
    
    return app