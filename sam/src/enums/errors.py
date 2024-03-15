from enum import Enum
from flask_babel import lazy_gettext

class Errors(Enum):
    INVALID_CREDENTIALS = lazy_gettext('Credenciais inválidas')
    ERROR_FORM = lazy_gettext("Problemas no formulário")
    FORBIDDEN = lazy_gettext('Acesso proibido')
    NOT_FOUND = lazy_gettext('Recurso não encontrado')
    INTERNAL_SERVER_ERROR = lazy_gettext('Erro interno do servidor')
    GENERIC_ERROR = lazy_gettext('Ocorreu algum erro')
    INVALID_LANGUAGE = lazy_gettext('Este idioma não existe')
    TOKEN_EXPIRED = lazy_gettext('O token de acesso da sessão de administrador expirou, faça login novamente')
    UNAUTHORIZED_ACCESS = lazy_gettext('Você não tem permissão para acessar esta página')
    SESSION_EXPIRED = lazy_gettext('Por segurança, seu acesso expirou por tempo prolongado de inatividade, faça login novamente para entrar no painel de controle')
    ERROR_GET_DATA = lazy_gettext('Não foi possivel recuperar os dados')
    FILE_PROBLEM = lazy_gettext("Ocorreu um erro ao salvar o arquivo")
    DB_SAVE_PROBLEM = lazy_gettext("Ocorreu um erro ao indexar o item no banco de dados")
    NO_IMAGES_FOUND = lazy_gettext("Sem mais imagens encontradas")
    NO_CHANGES = lazy_gettext("Nenhuma alteração feita")