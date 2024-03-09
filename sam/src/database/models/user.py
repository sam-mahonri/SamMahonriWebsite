from .. import bcrypt
from .... import mongo_client

class User:
    collection = mongo_client.get_database().user
    
    def __init__(self, username='', password=''):
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('utf-8') if password != '' else ''

    @classmethod
    def find_by_username(cls, username):
        try:
            return cls.collection.find_one({'username': username})
        except Exception as e:
            print(f'Error finding user: {str(e)}')
