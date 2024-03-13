from flask import Blueprint, render_template, request
from ..admin.forms import GalleryForm
dyna_bp = Blueprint('dyna', __name__, url_prefix='/dyna')
from flask_jwt_extended import jwt_required

from ..database import Gallery

BASE_COMMON = "components/common/"

@dyna_bp.route("/upload_image")
@jwt_required()
def upload_image(): 
    form = GalleryForm()
    callback = request.args.get('callback', 'self')
    id = request.args.get('id', 'image-uploader')
    url = request.args.get('url', '/api/gallery/image')
    return render_template(BASE_COMMON + "image_uploader.html", form = form, id = id, callback = callback, url = url)

@dyna_bp.route("/image-viewer")
def image_viewer():
    id = request.args.get('db-image-id', 'pop-img-viewer')
    url = request.args.get('url', '/favicon.ico')
    message = request.args.get('message', '')
    redirect_link = request.args.get('redirect_link', '')
    
    created_at = None
    updated_at = None
    
    got_image_data = None
    
    if id: got_image_data = Gallery.get_by_id(id)
    if got_image_data:
        url = got_image_data["image_links"]["original"]
        message = got_image_data.get("title", "")
        redirect_link = got_image_data.get("redirect_link", "")
        created_at = got_image_data.get("created_at", None)
        updated_at = got_image_data.get("updated_at", None)
        
    print(got_image_data)
    
    return render_template(BASE_COMMON + "image_viewer.html", id = id, message = message, url = url, redirect_link = redirect_link, created_at=created_at, updated_at=updated_at)