from ..universal.universal_many import UniversalMany
from .... import mongo_client

class Modalities(UniversalMany):
    collection = mongo_client.get_database()["modalities"]
    allowed_fields = {'title', 'description', 'type_value', 'image_link'}
