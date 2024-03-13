import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from ... import app
from .image_utils import compress_image, resize_image, crop_and_resize_image
from flask_babel import lazy_gettext

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_PATH = app.config['UPLOAD_PATH']
URL_BASE = app.config['URL_BASE']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(file, ignore_original=False, percent=40, ignore_cropped=False):
    load_dotenv()
    try:
        if file and allowed_file(file.filename):
            unique_filename = secure_filename(os.urandom(8).hex() + '_' + file.filename)
            file_path = os.path.join(UPLOAD_PATH, unique_filename)
            file.save(file_path)

            if file.content_type == 'image/gif':
                compressed_path = unique_filename
                resized_path = unique_filename
            else:
                compressed_path = compress_image(file_path)
                resized_path = resize_image(file_path, percent=percent) if not ignore_cropped else ''

                if ignore_original:
                    os.remove(file_path)

            return {
                'success': True,
                'url': f"{URL_BASE}gallery/image/{unique_filename}" if not ignore_original else f"{URL_BASE}gallery/image/{compressed_path}",
                'compressed_path': f"{URL_BASE}gallery/image/{os.path.basename(compressed_path)}",
                'resized_path': f"{URL_BASE}gallery/image/{os.path.basename(resized_path)}" if resized_path else f"{URL_BASE}image/{compressed_path}"
            }
        else:
            return {'success': False, 'message': lazy_gettext('O Arquivo não é uma imagem suportada.')}
    except Exception as e:
        return {'success': False, 'message': str(e)}
