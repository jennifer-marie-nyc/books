from flask import redirect, request
from flask_app import app
from flask_app.models.favorite import Favorite

@app.route('/favorites/create', methods=['POST'])
def create_favorite():
        Favorite.create(request.form)
        redirect_location = request.form['redirect']

        if redirect_location == 'users':
            this_user_id = request.form['user_id']
            return redirect(f'/users/{this_user_id}')
        
        elif redirect_location == 'books':
            this_book_id = request.form['book_id']
            return redirect(f'/books/{this_book_id}')