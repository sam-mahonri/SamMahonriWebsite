from enum import Enum
from flask_babel import lazy_gettext

class Success(Enum):
    SUCCESS_POST = lazy_gettext('Postagem criada com êxito!')
    SUCCESS_SAVED = lazy_gettext('Salvo com êxito!')