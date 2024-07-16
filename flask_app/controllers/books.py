from flask import render_template, redirect, request, url_for
from flask_app import app
from flask_app.models.book import Book
from flask_app.models import user

@app.route('/books')
def display_all_books():
    all_books = Book.get_all()
    return render_template('books.html', books=all_books)

@app.route('/new_book', methods=['POST'])
def create_book():
    Book.create(request.form)
    return redirect(url_for("display_all_books"))

@app.route('/books/<int:book_id>')
def show_book(book_id):
    selected_book = Book.get_book_with_favorites(book_id)
    all_users = user.User.get_all()
    """Display users that have NOT favorited this book in 
    add user to favorites select input"""
    users_not_favorited = []
    for one_user in all_users:
        if selected_book.favorites:
            """If book has favorites, append users who have NOT favorited it"""
            for i in range (0, len(selected_book.favorites)):
                if one_user.id == selected_book.favorites[i].id:
                    print(f'{one_user.first_name} {one_user.last_name} has favorited this book.')
                    break
                elif i == len(selected_book.favorites) - 1:
                    users_not_favorited.append(one_user)
        else:
            """If book has no favorites, include all users"""
            users_not_favorited = all_users

    return render_template('show_book.html', book=selected_book, users_not_favorited=users_not_favorited)