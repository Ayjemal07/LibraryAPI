from flask import Blueprint, request, jsonify, render_template
from app.helpers import token_required
from app.models import db, User, Book, book_schema, books_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/books', methods = ['POST'])
@token_required
def create_book(current_user_token):
    isbn = request.json['isbn']
    author_name = request.json['author']
    title = request.json['title']
    genre = request.json['genre']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    book = Book(isbn, author_name, title, genre, user_token = user_token )
    db.session.add(book)
    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)


@api.route('/books', methods = ['GET'])
@token_required
def get_books(current_user_token):
    a_user = current_user_token.token
    books= Book.query.filter_by(user_token = a_user).all()
    response = books_schema.dump(books)
    return jsonify(response)

@api.route('/books/<id>', methods = ['GET'])
@token_required
def get_single_book(current_user_token,id):
    book = Book.query.get(id)
    response = book_schema.dump(book)
    return jsonify(response)


@api.route('/books/<id>', methods = ['POST','PUT'])
@token_required
def update_book(current_user_token,id):
    book = Book.query.get(id) 
    book.isbn = request.json['isbn']
    book.author_name= request.json['author']
    book.title = request.json['title']
    book.genre = request.json['genre']
    book.user_token = current_user_token.token

    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)

@api.route('/books/<id>', methods = ['DELETE'])
@token_required
def delete_book(current_user_token, id):
    book = Book.query.get(id)
    if book.user_token!=current_user_token.token:
        return {"error":"This book does not belong to you"}
    db.session.delete(book)
    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)