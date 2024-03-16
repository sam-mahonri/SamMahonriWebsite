from flask import Blueprint, render_template, request
from ..admin.forms import GalleryForm, GalleryEditForm, DeleteItem, BaseCommissionType, EditCommissionType
macro_bp = Blueprint('macro', __name__, url_prefix='/macro')
from flask_jwt_extended import jwt_required

from ..database import Gallery, Modalities

BASE_COMMON = "components/common/"

@macro_bp.route("/delete-item")
@jwt_required()
def delete_item():
    item_id = request.args.get('item-id', '')
    route = request.args.get('route', '')
    callback = request.args.get('callback', '')
    form = DeleteItem()
    form.item_id.data = item_id
    return render_template(BASE_COMMON + "item_delete.html", form = form, callback = callback, route = route)

@macro_bp.route("/upload_image")
@jwt_required()
def upload_image(): 
    form = GalleryForm()
    callback = request.args.get('callback', 'self')
    id = request.args.get('id', 'image-uploader')
    url = request.args.get('url', '/api/gallery/image')
    return render_template(BASE_COMMON + "image_uploader.html", form = form, id = id, callback = callback, url = url)

@macro_bp.route("/edit_image")
@jwt_required()
def edit_image(): 
    form = GalleryEditForm()
    callback = request.args.get('callback', 'closeReloadSelf')
    id = request.args.get('id', '')
    url = request.args.get('url', '/api/gallery/image')
    
    got_image_data = None
    
    if id: got_image_data = Gallery.get_by_id(id)
    if got_image_data:
        form.title.data = got_image_data.get("title", "")
        form.redirect_link.data = got_image_data.get("redirect_link", "")
        form.is_artwork.data = got_image_data.get("is_artwork", False)
        form.image_id.data = id
    
    return render_template(BASE_COMMON + "image_edit.html", form = form, id = id, callback = callback, url = url)

@macro_bp.route("/image-viewer")
def image_viewer():
    id = request.args.get('db-image-id', '')
    url = request.args.get('url', '/favicon.ico')
    message = request.args.get('message', '')
    redirect_link = request.args.get('redirect_link', '')
    
    created_at = None
    updated_at = None
    
    got_image_data = None
    
    if id: got_image_data = Gallery.get_by_id(id)
    if got_image_data:
        image_urls = got_image_data["image_links"]
        message = got_image_data.get("title", "")
        redirect_link = got_image_data.get("redirect_link", "")
        created_at = got_image_data.get("created_at", None)
        updated_at = got_image_data.get("updated_at", None)
    
    return render_template(BASE_COMMON + "image_viewer.html", id = id, message = message, image_urls=image_urls, redirect_link = redirect_link, created_at=created_at, updated_at=updated_at)

@macro_bp.route("/create_modality")
@jwt_required()
def create_modality(): 
    form = BaseCommissionType()
    callback = request.args.get('callback', 'reloadModalities')
    id = request.args.get('id', 'new-comm-modality')
    url = request.args.get('url', '/api/commissions/modality')
    return render_template(BASE_COMMON + "modality_new.html", form = form, id = id, callback = callback, url = url)

@macro_bp.route("/edit_modality")
@jwt_required()
def edit_modality(): 
    form = EditCommissionType()
    callback = request.args.get('callback', 'onlyReloadModalities')
    slug = request.args.get('slug', '')
    url = request.args.get('url', '/api/commissions/modality')
    
    got_modality_data = None
    
    if slug: got_modality_data = Modalities.find_by_slug(slug)
    
    if got_modality_data:
        form.title.data = got_modality_data.get("title", "")
        form.description.data = got_modality_data.get("description", "")
        form.image_link.data = got_modality_data.get("image_link", "")
        form.type_value.data = got_modality_data.get("type_value", "")
        form.slug.data = slug
    
    return render_template(BASE_COMMON + "modality_edit.html", form = form, slug = slug, callback = callback, url = url)