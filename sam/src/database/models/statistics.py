from .... import mongo_client
from datetime import datetime

class Statistics:
    collection = mongo_client.get_database().statistics

    def __init__(self, accesses=0, arts=0, posts=0, created_at=None):
        self.accesses = accesses
        self.arts = arts
        self.posts = posts
        self.created_at = created_at or datetime.utcnow()

    def save(self):
        try:
            self.collection.insert_one({
                'accesses': self.accesses,
                'arts': self.arts,
                'posts': self.posts,
                'created_at': self.created_at
            })
        except Exception as e:
            print(f'Error saving statistics: {str(e)}')

    @classmethod
    def find(cls):
        document = cls.collection.find_one()
        return document if document else {'accesses': 0, 'arts': 0, 'posts': 0, 'created_at': None}

    @classmethod
    def update(cls, increment=None, decrement=None):
        try:
            if increment not in ['accesses', 'arts', 'posts']:
                raise ValueError("Invalid increment type. Use 'accesses', 'arts', or 'posts'.")
                
            update_value = 1
            if decrement:
                update_value = -1

            update_result = cls.collection.update_one(
                {},
                {'$inc': {increment: update_value}},
                upsert=False
            )
            if update_result.modified_count == 0:
                cls.collection.update_one(
                    {},
                    {'$set': {'accesses': 0, 'arts': 0, 'posts': 0, 'created_at': datetime.utcnow()}},
                    upsert=True
                )
            return True
        except Exception as e:
            print(f'Error updating statistics: {str(e)}')
            return False

    @classmethod
    def reset_weekly(cls):
        try:
            current_date = datetime.utcnow()
            last_update_document = cls.collection.find_one({}, {'created_at': 1})

            if last_update_document and 'created_at' in last_update_document:
                last_update_date = last_update_document['created_at']
                days_difference = (current_date - last_update_date).days

                if days_difference >= 7:
                    cls.collection.update_one(
                        {},
                        {'$set': {'accesses': 0, 'arts': 0, 'posts': 0, 'created_at': current_date}}
                    )
            else:
                cls.collection.insert_one({
                    'accesses': 0,
                    'arts': 0,
                    'posts': 0,
                    'created_at': current_date
                })

        except Exception as e:
            print(f'Error resetting weekly statistics: {str(e)}')