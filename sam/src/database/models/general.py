from ..universal.universal_one import UniversalOne

class GeneralSettings(UniversalOne):
    collection_name = "general"
    allowed_fields = {'title', 'description', 'warning_show', 'image_link', 'redirect_link', 'form_comms_link', 'total_slots', 'used_slots', 'comms_open'}
