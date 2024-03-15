from .... import mongo_client
from datetime import datetime
from bson import ObjectId
from ..universal import delete_file

class Gallery:
    collection = mongo_client.get_database().gallery

    @classmethod
    def create(cls, title, original_link, compressed_link, thumbnail_link, redirect_link, is_artwork):
        image_data = {
            'title': title,
            'image_links': {
                'original': original_link,
                'compressed': compressed_link,
                'thumbnail': thumbnail_link
            },
            'redirect_link': redirect_link,
            'is_artwork': is_artwork,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        result = cls.collection.insert_one(image_data)
        return str(result.inserted_id)

    @classmethod
    def update(cls, image_id, title=None, original_link=None, compressed_link=None, thumbnail_link=None, redirect_link=None, is_artwork=None):
        update_data = {'updated_at': datetime.now()}
        if title is not None: update_data['title'] = title
        if original_link is not None: update_data['image_links.original'] = original_link
        if compressed_link is not None: update_data['image_links.compressed'] = compressed_link
        if thumbnail_link is not None: update_data['image_links.thumbnail'] = thumbnail_link
        if redirect_link is not None: update_data['redirect_link'] = redirect_link
        if is_artwork is not None: update_data['is_artwork'] = is_artwork
        result = cls.collection.update_one({'_id': ObjectId(image_id)}, {'$set': update_data})
        return result.modified_count > 0

    @classmethod
    def find(cls, page=1, per_page=9, is_artwork=None, title=None):
        filter_query = {}
        if is_artwork is not None:
            filter_query['is_artwork'] = bool(is_artwork)
        if title:
            filter_query['title'] = {'$regex': title, '$options': 'i'}
        skip = (page - 1) * per_page
        images = cls.collection.find(filter_query).sort('created_at', -1).skip(skip).limit(per_page)
        
        # Convertendo os ObjectIds para strings
        images = [{**image, '_id': str(image['_id'])} for image in images]
        
        return images

    @classmethod
    def get_by_id(cls, image_id):
        image = cls.collection.find_one({'_id': ObjectId(image_id)})
        if image:
            image['_id'] = str(image['_id'])
        return image
    
    @classmethod
    def delete(cls, image_id):
        
        image = cls.collection.find_one({'_id': ObjectId(image_id)})
        result = {"deleted_count": 0}
        fully_deleted = False
        try:
            if image:
                errors = 0
                for i in image['image_links'].keys():
                    if not delete_file.delete_fileurl(image['image_links'][i]): errors += 1
                if not errors > 2: 
                    result = cls.collection.delete_one({'_id': ObjectId(image_id)})
                    fully_deleted = result.deleted_count > 0
        except:
            pass
        
        return image and fully_deleted
