from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, FloatField, ValidationError, EmailField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Length, EqualTo, InputRequired, NumberRange, Optional, URL
from flask_babel import lazy_gettext as _

class CustomFloatField(FloatField):
    def process_formdata(self, valuelist):
        if valuelist:
            try:
                value = float(valuelist[0].replace(',', '.'))
                self.data = value
            except ValueError:
                raise ValidationError(_('Valor real não válido'))
        else:
            self.data = None

class GeneralSettingsForm(FlaskForm):
    title = StringField(_('Título do aviso'), validators=[Length(max=64)])
    description = TextAreaField(_('Descrição do aviso'), validators=[Length(min=0, max=1000)])
    warning_show = BooleanField(_('Mostrar aviso'))
    image_link = StringField(_('Link da imagem do banner'), validators=[Optional(), URL()])
    redirect_link = StringField(_('Link de redirecionamento'), validators=[Optional(), URL()])
    form_comms_link = StringField(_('Link do formulário de contato para comissões'), validators=[Optional(), URL(), Length(min=3, max=100)])
    total_slots = IntegerField(_('Número total de slots'), render_kw={"type": "number"}, default=100)
    used_slots = IntegerField(_('Slots usados'), render_kw={"type": "number"}, default=0)
    comms_open = BooleanField(_('Comissões abertas'))
    
    def validate_used_slots(self, field):
        if field.data is not None and self.total_slots.data is not None:
            if field.data > self.total_slots.data:
                raise ValidationError(_('Os slots utilizados não podem ser maiores que o total de slots.'))

class BaseCommissionType(FlaskForm):
    title = StringField(_('Título'), validators=[InputRequired(), Length(min=3, max=100)])
    description = StringField(_('Descrição'), validators=[InputRequired(), Length(min=3, max=100)])
    type_value = CustomFloatField(_('Valor máximo do tipo'), validators=[InputRequired()], render_kw={"type": "float"})
    image_link = StringField(_('Link da imagem de exemplo do tipo'), validators=[InputRequired(), URL()])

class EditCommissionType(BaseCommissionType):
    slug = HiddenField(validators=[InputRequired()])

class PostForm(FlaskForm):
    title = StringField(_('Título'), validators=[InputRequired(), Length(min=3, max=100)])
    image_link = StringField(_('Link da imagem do banner'), validators=[Optional(), URL()])
    tags = StringField(_('Tags (separadas por vírgula)'), validators=[Optional()])
    content = TextAreaField(_('Conteúdo'), validators=[InputRequired(), Length(min=3, max=10000)])

class BaseGalleryForm(FlaskForm):
    title = StringField(_('Nome da imagem'), validators=[InputRequired(), Length(max=20)])
    is_artwork = BooleanField(_('Listar na galeria de artes'))
    redirect_link = StringField(_('Link alternativo (Ex.: Postagem em rede social)'), validators=[Optional(), URL()])

class GalleryForm(BaseGalleryForm):
    image = FileField(_('Arquivo de imagem'), validators=[InputRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'gif'], _('Apenas imagens do tipo .jpg, .png, .gif e .jpeg!'))])

class GalleryEditForm(BaseGalleryForm):
    image_id = HiddenField(validators=[InputRequired()])
    pass

class DeleteItem(FlaskForm):
    item_id = HiddenField(validators=[InputRequired()])
    please_delete = BooleanField(_('Excluir item?'))