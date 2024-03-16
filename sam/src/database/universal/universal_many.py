from .... import mongo_client
from datetime import datetime
from slugify import slugify

class UniversalMany:
    allowed_fields = {'title', 'content', 'author'}  # Campos permitidos
    collection = mongo_client.get_database()["posts"]


    @classmethod
    def create(cls, data):
        try:
            if all(field in cls.allowed_fields for field in data.keys()):
                if 'title' not in data:
                    print("Error: 'title' field is required.")
                    return None

                original_slug = slugify(data['title'])
                slug = original_slug
                suffix = 1
                while cls.collection.find_one({'slug': slug}):
                    slug = f"{original_slug}-{suffix}"
                    suffix += 1

                # Verificar se existe o campo 'tag' e transformar em uma lista de tags
                if 'tag' in data:
                    data['tag'] = data['tag'].split(',')

                data['slug'] = slug
                data['created_at'] = datetime.now()
                
                cls.collection.insert_one(data)
                return slug
            else: 
                return None
        except Exception as e:
            print(f"Error creating document: {str(e)}")
            return None

    @classmethod
    def update_by_slug(cls, slug, data):
        try:
            data['updated_at'] = datetime.now() 

            # Verificar se existe o campo 'tag' e transformar em uma lista de tags
            if 'tag' in data:
                data['tag'] = data['tag'].split(',')

            cls.collection.update_one({'slug': slug}, {'$set': data})
            return True
        except Exception as e:
            print(f"Error updating document: {str(e)}")
            return False

    @classmethod
    def find_by_slug(cls, slug):
        try:
            return cls.collection.find_one({'slug': slug})
        except Exception as e:
            print(f"Error finding document: {str(e)}")
            return None

    @classmethod
    def list_all(cls, per_page=4, page=1, query=None):
        try:
            if query is None:
                query = {}

            total_posts = cls.collection.count_documents(query)
            total_pages = (total_posts + per_page - 1) // per_page
            if page > total_pages:
                return []

            skip_count = per_page * (page - 1)
            posts = cls.collection.find(query).sort([('created_at', -1)]).skip(skip_count).limit(per_page)
            
            posts = [{**post, '_id': str(post['_id'])} for post in posts]
            
            return list(posts), total_pages
        except Exception as e:
            print(f"Error listing documents: {str(e)}")
            return [], 0

    @classmethod
    def delete_by_slug(cls, slug):
        try:
            result = cls.collection.delete_one({'slug': slug})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting document: {str(e)}")
            return False


# Exemplo de pesquisa por título
# title_query = {'title': {'$regex': 'exemplo', '$options': 'i'}}  # Pesquisa por títulos que contenham 'exemplo' (case-insensitive)

# Exemplo de pesquisa por tag
# tag_query = {'tag': 'python'}  # Pesquisa por postagens que possuam a tag 'python'

# Exemplo de pesquisa por título e tag combinados
# combined_query = {
#     '$and': [
#         {'title': {'$regex': 'exemplo', '$options': 'i'}},  # Pesquisa por títulos que contenham 'exemplo' (case-insensitive)
#         {'tag': 'python'}  # Pesquisa por postagens que possuam a tag 'python'
#     ]
# }