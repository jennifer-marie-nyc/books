from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book
from pprint import pprint

class User:
    db = 'books_schema'

    def __init__(self, data):
        self.id = data['id']
        self.first_name =  data['first_name']
        self.last_name = data['last_name']
        self.favorites = []

    @staticmethod
    def create(form_data):
        query = """
            INSERT INTO users 
            (first_name, last_name)
            VALUES (%(first_name)s, %(last_name)s);
        """
        user_id = connectToMySQL('books_schema').query_db(query, form_data)

        return user_id

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM users;'
        results = connectToMySQL(cls.db).query_db(query)
        all_users = []
        for user in results:
            all_users.append(cls(user))

        return all_users
    
    @classmethod
    def get_user_with_favorites(cls, user_id):
        query = """
            SELECT * FROM users
            LEFT JOIN favorites 
            ON favorites.user_id = users.id
            LEFT JOIN books
            ON books.id = favorites.book_id
            WHERE users.id = %(id)s
        """
        data = {
            'id': user_id
        }
        results = connectToMySQL(cls.db).query_db(query, data)

        user = cls(results[0])

        if results[0]['books.id']:
            print('This user has favorites.')
            for row_from_db in results:
                book_data = {
                    'id': row_from_db['books.id'],
                    'title': row_from_db['title'],
                    'num_of_pages': row_from_db['num_of_pages']
                } 
                user.favorites.append(book.Book(book_data))

        return user
        
