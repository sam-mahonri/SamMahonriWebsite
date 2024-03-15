from enum import Enum
from flask_babel import lazy_gettext

class Success(Enum):
    SUCCESS_POST = lazy_gettext('Postagem criada com êxito!')
    SUCCESS_SAVED = lazy_gettext('Salvo com êxito!')
    SUCCESS_UPLOAD = lazy_gettext('Arquivo enviado com êxito!')
    SUCCESS_LOADED = lazy_gettext('Carregado com êxito!')
    SUCCESS_WELCOME = lazy_gettext('Bem-vindo!')
    SUCCESS_DELETED = lazy_gettext('Item excluído com êxito!')