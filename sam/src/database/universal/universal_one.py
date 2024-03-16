from .... import mongo_client
from datetime import datetime

# Classe pai para modelos que trabalham com apenas um documento, você pode usar para guardar informações fixas
# Foi originalmente implementada para trabalhar com conteúdo "estático" de páginas ou configurações globais de um site

class UniversalOne:
    allowed_fields = {} # Campos permitidos para manter a consistência do sistema, se {} então qualquer campo é permitido
    collection = mongo_client.get_database()["general"]
    
    @classmethod
    def update(cls, data={}):
        try:
            if cls.allowed_fields == {} or all(field in cls.allowed_fields for field in data.keys()):
                document = cls.find()
                data['updated_at'] = datetime.now() 
                if document is None: data['created_at'] = datetime.now() 
                cls.collection.update_one({}, {'$set': data}, upsert=True)
                
                return True
            else:
                rejected_fields = [field for field in data.keys() if field not in cls.allowed_fields]
                error_message = f"Error: The following fields are not allowed: {', '.join(rejected_fields)}"
                print(error_message)
                return False
        except Exception as e:
            print(f'Error updating document: {str(e)}')
            return False

    @classmethod
    def find(cls):
        try:
            return cls.collection.find_one()
        except Exception as e:
            print(f'Error finding document: {str(e)}')
            return None