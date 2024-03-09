from enum import Enum
from flask_babel import lazy_gettext

class Warnings(Enum):
    IMAGE_FAILURE = lazy_gettext('Não foi possível carregar corretamente o arquivo da imagem')