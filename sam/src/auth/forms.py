from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, InputRequired, Length
from flask_babel import gettext, _, lazy_gettext

class LoginForm(FlaskForm):
    username = StringField(lazy_gettext('Nome de usuário'), validators=[InputRequired(), Length(min=4, max=50)])
    password = PasswordField(lazy_gettext('Senha'), validators=[InputRequired(), Length(min=6)])