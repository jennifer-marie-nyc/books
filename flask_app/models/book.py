from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from pprint import pprint

class Book:
    db = 'books_schema'

    def __init__(self, data):
        self.id = data['id']
        self.title =  data['title']
        self.num_of_pages = data['num_of_pages']
        self.favorites = []

    @staticmethod
    def create(form_data):
        query = """
            INSERT INTO books
            (title, num_of_pages)
            VALUES (%(title)s, %(num_of_pages)s)
        """
        book_id = connectToMySQL('books_schema').query_db(query, form_data)

        return book_id

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM books'

        results = connectToMySQL(cls.db).query_db(query)
        # pprint(f'All books: {results}')

        all_books = []
        for book in results:
            all_books.append(cls(book))

        return all_books
    
    @classmethod
    def get_book_with_favorites(cls, book_id):
        query = """
            SELECT * FROM books
            LEFT JOIN favorites
            ON favorites.book_id = books.id
            LEFT JOIN users
            on favorites.user_id = users.id
            WHERE books.id = %(id)s
        """
        data = {
            'id': book_id
        }
        results = connectToMySQL(cls.db).query_db(query, data)

        book = cls(results[0])

        if results[0]['users.id']:
            print('This book has been favorited.')
            for row_from_db in results:
                pprint(row_from_db)
                user_data = {
                    'id': row_from_db['users.id'],
                    'first_name': row_from_db['first_name'],
                    'last_name': row_from_db['last_name']
                }
                book.favorites.append(user.User(user_data))

        return book
