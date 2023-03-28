from flask import Blueprint, jsonify, request
from app import mongo
from flask_pymongo import ObjectId
from schemas.books import validate_provided_book, validate_local_book
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.decorators import user_access_required
from utils.users import get_user_id, get_username, validate_admin
from utils.others import validate_category


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
    
    
    
    if not validate_provided_book(book):
        return jsonify({'msg': 'Invalid book','status': {
            'name': 'not_created',
            'action': 'create',
            'create': False
        }})
    
    id = mongo.db.books.insert_one({
        'user_id': user_id,
        'name': book.get('name'),
        'description': book.get('description'),
        'author': get_username(user_id),
        'categories': book.get('categories')
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
@jwt_required(optional=True)
def getBooks():
    
    user_id = get_user_id(get_jwt_identity())

    Filter = request.args.get('filter')
    if not Filter:
        books = mongo.db.books.find({})
    else:
        if Filter.startswith('@'):
            Filter = Filter.replace('@', '')
            user_id = mongo.db.users.find_one({'username': Filter}).get('_id')
            books = mongo.db.books.find({'user_id': user_id})
        elif Filter.startswith('$'):
            if not user_id:
                return jsonify({'msg': '$ filters are not allowed if JWT token is not provided',
                        'status': {
                            'name': 'bad_request',
                            'action': 'get',
                            'get': False
                        }
                        }), 400
            if Filter == '$me':
                books = mongo.db.books.find({'user_id': user_id})
            elif Filter == '$others':
                books = mongo.db.books.find({'user_id': {'$nin': [user_id]}})
            elif Filter == '$all':
                books = mongo.db.books.find({})  
            else:
                return jsonify({'msg': f'unknow @ filter "{Filter}"',
                                'status':{
                                    'name': 'bad_request',
                                    'action': 'get',
                                    'get': False
                                }
                                }), 400
        elif Filter.startswith('#'):
            category = Filter[1:]
            if not validate_category(category):
                return jsonify({'msg': f'invalid category "{category}"',
                                'status': {
                                    'name': 'bad_request',
                                    'action': 'get',
                                    'get': False
                                }}), 400
            books = mongo.db.books.find({'categories': {'$elemMatch': {'$eq': category}}})
    
    books = list(books)        
    return jsonify( {
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
            'author': book.get('author'),
            'categories': book.get('categories')
            },books))
        })

@books_blueprint.route('/books/<id>', methods = ['GET'])
@jwt_required(optional=True)
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
                'author': book.get('author'),
                'categories': book.get('categories')
            }
    })

@books_blueprint.route('/books/<id>', methods = ['DELETE'])
@jwt_required()
@user_access_required(action='delete',name='not_found',pass_user_id = True)
def deleteBook(id,user_id):
    book = mongo.db.books.find_one({'_id': ObjectId(id)})
    if not book:
        return jsonify({
            'msg': 'Book not found',
            'status': {
                'name': 'not_found',
                'action': 'delete',
                'delete': False
                }   
            })
    
    if validate_admin(user_id):
        mongo.db.books.delete_one({'_id': ObjectId(id)})
        return jsonify({'msg': 'Book deleted',
                    'status': {
                        'name': 'deleted',
                        'action': 'delete',
                        'delete': True
                    }})

    if book.get('user_id') != user_id:
        return jsonify({
            'msg': 'This book does not belong to you',
            'status': {
                'name': 'not_authorized',
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

@books_blueprint.route('/books/<id>', methods = ['PUT'])
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
    
    db_book = mongo.db.books.find_one({'_id': ObjectId(id)})
    if not db_book:
        return jsonify({
            'msg': 'Book not found',
            'status': {
                'name': 'not_found',
                'action': 'delete',
                'delete': False
                }   
            })
    if db_book.get('user_id') != user_id:
        return jsonify({
            'msg': 'This book does not belong to you',
            'status': {
                'name': 'not_authorized',
                'action': 'update',
                'update': False
            }
        })
    
    if not validate_provided_book(book):
        return jsonify({'msg': 'Invalid book','status': {
            'name': 'not_updated',
            'action': 'update',
            'update': False
        }})
    
    mongo.db.books.update_one({'user_id': user_id,'_id': ObjectId(id)}, {'$set': {
        'name': book.get('name'),
        'description': book.get('description'),
        'categories': book.get('categories')
    }})
    return jsonify({
        'msg': 'Book updated',
        'status': {
            'name': 'updated',
            'action': 'update',
            'update': True
        }
    })