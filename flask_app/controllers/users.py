from flask import render_template, redirect, request, url_for
from flask_app import app
from flask_app.models.user import User
from flask_app.models import book
from pprint import pprint

@app.route('/users')
def display_all_users():
    all_users = User.get_all()
    return render_template('users.html', users = all_users)

@app.route('/new_user', methods=['POST'])
def create_user():
    User.create(request.form)
    return redirect(url_for("display_all_users"))

@app.route('/users/<int:user_id>')
def show_user(user_id):
    selected_user = User.get_user_with_favorites(user_id)
    all_books = book.Book.get_all()
    """Display books user has NOT favorited in add favorite select input"""
    not_favorited = []
    for one_book in all_books:
        if selected_user.favorites:
            """If user has favorites, append user's favorites"""
            for i in range (0, len(selected_user.favorites)):
                if one_book.title == selected_user.favorites[i].title:
                    print(f'User has favorited {one_book.title}')
                    break
                elif i == len(selected_user.favorites) - 1:
                    not_favorited.append(one_book)
        else:
            """If user has no favorites, include all books"""
            not_favorited = all_books

    for non_fav in not_favorited:
        pprint(non_fav.title)

    return render_template('show_user.html', user=selected_user, books_not_favorited=not_favorited)