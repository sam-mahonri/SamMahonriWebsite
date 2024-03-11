from flask import Blueprint, render_template, request
from ..admin.forms import GalleryForm
dyna_bp = Blueprint('dyna', __name__, url_prefix='/dyna')
from flask_jwt_extended import jwt_required
BASE_COMMON = "components/common/"

@dyna_bp.route("/upload_image")
@jwt_required()
def upload_image(): 
    form = GalleryForm()
    callback = request.args.get('callback', 'self')
    id = request.args.get('id', 'image-uploader')
    url = request.args.get('url', '/api/gallery/image')
    return render_template(BASE_COMMON + "image_uploader.html", form = form, id = id, callback = callback, url = url)