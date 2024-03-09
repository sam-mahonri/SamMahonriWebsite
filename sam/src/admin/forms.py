from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, FloatField, ValidationError, EmailField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, InputRequired, NumberRange, Optional, URL
from flask_babel import gettext, _, lazy_gettext

class CustomFloatField(FloatField):
    def process_formdata(self, valuelist):
        if valuelist:
            try:
                value = float(valuelist[0].replace(',', '.'))
                self.data = value
            except ValueError:
                raise ValidationError('Not a valid float value')
        else:
            self.data = None

class GeneralSettingsForm(FlaskForm):
    title = StringField(lazy_gettext('Título do aviso'), validators=[Length(max=20)])
    description = TextAreaField(lazy_gettext('Descrição do aviso'), validators=[Length(min=0, max=1000)])
    warning_show = BooleanField(lazy_gettext('Mostrar aviso'))
    image_link = StringField(lazy_gettext('Link da imagem do banner'), validators=[Optional(), URL()])
    redirect_link = StringField(lazy_gettext('Link de redirecionamento'), validators=[Optional(), URL()])
    form_comms_link = StringField(lazy_gettext('Link do formulário de contato para comissões'), validators=[Optional(), URL(), Length(min=3, max=100)])
    total_slots = IntegerField(lazy_gettext('Número total de slots'), render_kw={"type": "number"}, default=100)
    used_slots = IntegerField(lazy_gettext('Slots usados'), render_kw={"type": "number"}, default=0)
    comms_open = BooleanField(lazy_gettext('Comissões abertas'))
    
    def validate_used_slots(self, field):
        if field.data is not None and self.total_slots.data is not None:
            if field.data > self.total_slots.data:
                raise ValidationError(lazy_gettext('Os slots utilizados não podem ser maiores que o total de slots.'))

class CommissionType(FlaskForm):
    title = StringField(lazy_gettext('Título'), validators=[InputRequired(), Length(min=3, max=100)])
    type_value = CustomFloatField(lazy_gettext('Valor máximo do tipo'), validators=[InputRequired()])
    image_link = StringField(lazy_gettext('Link da imagem de exemplo do tipo'), validators=[Optional(), URL()])

class PostForm(FlaskForm):
    title = StringField(lazy_gettext('Título'), validators=[InputRequired(), Length(min=3, max=100)])
    image_link = StringField(lazy_gettext('Link da imagem do banner'), validators=[Optional(), URL()])
    tags = StringField(lazy_gettext('Tags (separadas por vírgula)'), validators=[Optional()])
    content = TextAreaField(lazy_gettext('Conteúdo'), validators=[InputRequired(), Length(min=3, max=10000)])

class GalleryForm(FlaskForm):
    title = StringField(lazy_gettext('Nome da imagem'), validators=[Length(max=20)])
    is_artwork = BooleanField(lazy_gettext('Listar na galeria de artes'))
    image = FileField('image', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], lazy_gettext('Apenas imagens do tipo .jpg, .png, .gif e .jpeg!'))])
