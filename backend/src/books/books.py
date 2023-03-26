from flask import Blueprint, jsonify, request
from app import mongo
from flask_pymongo import ObjectId
from schemas.books import validate_book
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.decorators import user_access_required

books_blueprint = Blueprint('books', __name__)


@books_blueprint.route('/books', methods = ['POST'])
@jwt_required()
@user_access_required('create', 'not_created', pass_user_id = True)
def createBook(user_id):
    book = request.json.get('book')
    if not book:
        return jsonify({'msg': 'No book provided','status': {
            'name': 'not_created',
            'action': 'create',
            'create': False
            }}), 400
    
    
    
    if not validate_book(book):
        return jsonify({'msg': 'Invalid book','status': {
            'name': 'not_created',
            'action': 'create',
            'create': False
        }})
    
    id = mongo.db.books.insert_one({
        'user_id': user_id,
        'name': book.get('name'),
        'description': book.get('description'),
        'author': book.get('author')
    })
    return jsonify({'msg': 'Book created','status': {
        'name': 'created',
        'action': 'create',
        'create': True
        },
        'data': {
            'id': str(id.inserted_id),
        }
        })
    

@books_blueprint.route('/books', methods = ['GET'])
@jwt_required()
@user_access_required(action='get',name='retrieved',pass_user_id = True)
def getBooks(user_id):
    poster = request.args.get('poster')
    if not poster:
        books = mongo.db.books.find({})
    else:
        if poster == '@me':
            books = mongo.db.books.find({'user_id': user_id})
        elif poster == '@others':
            books = mongo.db.books.find({'user_id': {'$nin': [user_id]}})   
        else:
            user_id = mongo.db.users.find_one({'username': poster}).get('_id')
            books = mongo.db.books.find({'user_id': user_id})
    return jsonify({
        'msg': 'Books retrieved',
        'status': {
            'name': 'retrieved',
            'action': 'get',
            'get': True
        },
        'data': list(map(lambda book: {
            'id': str(book.get('_id')),
            'name': book.get('name'),
            'description': book.get('description'),
            'author': book.get('author')
            },books))
    })

@books_blueprint.route('/books/<id>', methods = ['GET'])
@jwt_required()
@user_access_required(action='get',name='retrieved',pass_user_id = True)
def getBook(id):
    book = mongo.db.books.find_one({'_id': ObjectId(id)})
    if not book:
        return jsonify({'msg': 'Book not found','status': {
            'name': 'not_found',
            'action': 'get',
            'get': False
        }})
    
    return jsonify({
            'msg': 'Book retrieved',
            'status': {
                'name': 'retrieved',
                'action': 'get',
                'get': True
            },
            'data':{
                '_id': str(ObjectId(book['_id'])),
                'name': book.get('name'),
                'description': book.get('description'),
                'author': book.get('author')
            }
    })

@books_blueprint.route('/books/<id>', methods = ['DELETE'])
@jwt_required()
@user_access_required(action='delete',name='not_found',pass_user_id = True)
def deleteBook(id,user_id):
    book = mongo.db.books.find_one({'user_id': user_id,'_id': ObjectId(id)})
    if not book:
        return jsonify({
            'msg': 'Book not found',
            'status': {
                'name': 'not_found',
                'action': 'delete',
                'delete': False
                }   
            })
    
    mongo.db.books.delete_one({'user_id': user_id,'_id': ObjectId(id)})
    return jsonify({'msg': 'Book deleted',
                    'status': {
                        'name': 'deleted',
                        'action': 'delete',
                        'delete': True
                    }})

@books_blueprint.route('/book/<id>', methods = ['PUT'])
@jwt_required()
@user_access_required(action='update',name='not_updated',pass_user_id = True)
def updateBook(id,user_id):
    book = request.json.get('book')
    if not book:
        return jsonify({'msg': 'No book provided','status': {
            'name': 'not_updated',
            'action': 'update',
            'update': False
        }})
    
    book = mongo.db.books.find_one({'user_id': user_id,'_id': ObjectId(id)})
    if not book:
        return jsonify({
            'msg': 'Book not found',
            'status': {
                'name': 'not_found',
                'action': 'delete',
                'delete': False
                }   
            })
    
    if not validate_book(book):
        return jsonify({'msg': 'Invalid book','status': {
            'name': 'not_updated',
            'action': 'update',
            'update': False
        }})
    
    mongo.db.books.update_one({'user_id': user_id,'_id': ObjectId(id)}, {'$set': {
        'name': book.get('name'),
        'description': book.get('description'),
        'author': book.get('author')
    }})
    return jsonify({
        'msg': 'Book updated',
        'status': {
            'name': 'updated',
            'action': 'update',
            'update': True
        }
    })