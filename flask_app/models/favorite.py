from flask_app.config.mysqlconnection import connectToMySQL

class Favorite:
    db = 'books_schema'

    @classmethod
    def create(cls, form_data):
        """Creates a favorite in the database"""
        query = """
        INSERT INTO favorites
        (user_id, book_id)
        VALUES
        (%(user_id)s, %(book_id)s)
        """

        favorite_id = connectToMySQL(cls.db).query_db(query, form_data)

        return favorite_id