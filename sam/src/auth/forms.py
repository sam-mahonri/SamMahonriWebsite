from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, InputRequired, Length
from flask_babel import lazy_gettext as _

class LoginForm(FlaskForm):
    username = StringField(_('Nome de usuário'), validators=[InputRequired(), Length(min=4, max=50)])
    password = PasswordField(_('Senha'), validators=[InputRequired(), Length(min=6)])