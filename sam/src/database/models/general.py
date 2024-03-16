from ..universal.universal_one import UniversalOne
from .... import mongo_client

class GeneralSettings(UniversalOne):
    collection = mongo_client.get_database()["general"]
    allowed_fields = {'title', 'description', 'warning_show', 'image_link', 'redirect_link', 'form_comms_link', 'total_slots', 'used_slots', 'comms_open'}
