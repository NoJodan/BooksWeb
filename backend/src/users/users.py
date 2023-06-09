import base64
from flask import request, jsonify, blueprints
from app import mongo, app
from flask_pymongo import ObjectId
from utils.others import process_profile_image, delete_profile_image, send_profile_image
from utils.passwords import check_password, get_password
from utils.users import validate_username, validate_user, get_username, validate_user_by_id, get_user_id, validate_admin, validate_email
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.decorators import user_access_required
import datetime
from flask_jwt_extended import create_access_token
from schemas.users import validate_user as validate_user_schema

users_blueprint = blueprints.Blueprint('users', __name__)
PROFILE_IMAGES_PATH = app.config['USERS_PROFILE_IMAGES_PATH']


@users_blueprint.route('/users/<username>', methods=['GET'])
@jwt_required(optional=True)
def getUserData(username):
    user = mongo.db.users.find_one({'username': username})
    if not user:
        return jsonify({'msg': 'User not found', 'status': {
            'name': 'not_found',
            'action': 'get',
            'get': False
        }})
    
    image_b64 = send_profile_image(user.get('profile_image'))
    
    return jsonify({
        'msg': 'User retrieved',
        'status': {
            'name': 'retrieved',
            'action': 'get',
            'get': True
        },
        'data': {
            '_id': str(ObjectId(user['_id'])),
            'username': user.get('username'),
            'email': user.get('email'),
            'about': user.get('about'),
            'books_owned': user.get('books_owned'),
            'followers': user.get('followers'),
            'following': user.get('following'),
            'profile_image': user.get('profile_image'),
            'created_at': user.get('created_at'),
            'image_b64': image_b64
        }
    })


@users_blueprint.route('/users/profile', methods=['GET'])
@jwt_required()
def getProfile():
    user_id = get_user_id(get_jwt_identity())
    user = mongo.db.users.find_one({'_id': user_id})
    if not user:
        return jsonify({'msg': 'User not found', 'status': {
            'name': 'not_found',
            'action': 'get',
            'get': False
        }})
    
    image_b64 = send_profile_image(user.get('profile_image'))
    
    return jsonify({
        'msg': 'User retrieved',
        'status': {
            'name': 'retrieved',
            'action': 'get',
            'get': True
        },
        'data': {
            '_id': str(ObjectId(user['_id'])),
            'username': user.get('username'),
            'email': user.get('email'),
            'about': user.get('about'),
            'books_owned': user.get('books_owned'),
            'followers': user.get('followers'),
            'following': user.get('following'),
            'profile_image': user.get('profile_image'),
            'created_at': user.get('created_at'),
            'image_b64': image_b64
        }
    })


@users_blueprint.route('/users/<user>', methods=['DELETE'])
@jwt_required()
@user_access_required('delete', 'not_deleted', pass_user_id=True)
def deleteUser(user, user_id):
    if not validate_admin(user_id):
        return jsonify({'msg': 'You are not administrator',
                        'status': {
                            'name': 'not_authorized',
                            'action': 'delete',
                            'delete': False
                        }
                        }), 401
        
    if not validate_user_by_id(user):
        return jsonify({'msg': 'User does not exist',
                        'status': {
                            'name': 'not_found',
                            'action': 'delete',
                            'delete': False
                        }
                        }), 401

    books = mongo.db.books.find({'user_id': ObjectId(user)})
    if list(books) != []:
        return jsonify({'msg': 'Cannot delete user with books',
                        'status': {
                            'name': 'data_conflict',
                            'action': 'delete',
                            'delete': False
                        }
                        }), 409

    profile_image = mongo.db.users.find_one({'_id': ObjectId(user)}).get('profile_image')
    if profile_image != "default.jpg":
        delete_profile_image(profile_image)

    mongo.db.users.delete_one({'_id': ObjectId(user)})
    return jsonify({'msg': 'User deleted successfully',
                    'status': {
                        'name': 'deleted',
                        'action': 'delete',
                        'delete': True
                    }})


@users_blueprint.route('/users', methods=['PUT'])
@jwt_required()
@user_access_required('update', 'not_updated', pass_user_id=True)
def updateUser(user_id):
    if not validate_user_by_id(user_id):
        return jsonify({'msg': 'User does not exist',
                        'status': {
                            'name': 'not_found',
                            'action': 'update',
                            'update': False
                        }
                        }), 401

    user = request.json.get('user')
    if not user:
        return jsonify({'msg': 'Missing user',
                        'status': {
                            'name': 'invalid_data',
                            'action': 'update',
                            'update': False
                        }}), 400

    if not validate_user_schema(user):
        return jsonify({'msg': 'Invalid user',
                        'status': {
                            'name': 'invalid_data',
                            'action': 'update',
                        }}), 400

    set_user = {}
    set_user['username'] = user.get('username') if user.get('username') else get_username(user_id)
    if user.get('password'):
        set_user['password_hash'] = get_password(user.get('password'))
    if user.get('profile_image'):
        previous_profile_image = mongo.db.users.find_one(
            {'_id': user_id}).get('profile_image')
        if previous_profile_image != "default.jpg":
            delete_profile_image(previous_profile_image)
        set_user['profile_image'] = process_profile_image(
            user.get('profile_image'))
    mongo.db.users.update_one({'_id': user_id}, {'$set': set_user})

    return jsonify({'msg': 'User updated successfully',
                    'status': {
                        'name': 'updated',
                        'action': 'update',
                        'update': True
                    }
                    })


@users_blueprint.route('/users', methods=['GET'])
def login():
    auth = request.authorization
    user = mongo.db.users.find_one({'username': auth.username})

    stay_loged_in = request.args.get('stay_loged_in')

    if stay_loged_in == "true":
        expires_delta = datetime.timedelta(days=7)
    else:
        expires_delta = app.config['JWT_ACCESS_TOKEN_EXPIRES']

    if not user:
        return jsonify({'msg': 'User does not exist',
                        'status': {
                            'name': 'not_found',
                            'action': 'login',
                            'login': False
                        }
                        }), 401

    if auth and check_password(auth.password, user['password_hash']):
        token = create_access_token(
            identity=auth.username, expires_delta=expires_delta)

        return jsonify({'msg': 'User logged in successfully',
                        'status': {
                            'name': 'logged_in',
                            'action': 'login',
                            'login': True
                        },
                        'data': {
                            'token': token
                        }
                        })

    return jsonify({'msg': 'Invalid credentials',
                    'status': {
                        'name': 'invalid_data',
                        'action': 'login',
                        'login': False
                    }
                    }), 401


@users_blueprint.route('/users', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')

    if not username or not password or not email:
        return jsonify({'msg': 'Username, email or password missing',
                        'status': {
                            'name': 'invalid_data',
                            'action': 'register',
                            'register': False
                        }
                        }), 400

    if validate_user(username):
        return jsonify({'msg': 'Username already exists',
                        'status': {
                            'name': 'data_conflict',
                            'action': 'register',
                            'register': False
                        }
                        }), 400
    
    if validate_email(email):
        return jsonify({'msg': 'Email already exists',
                        'status': {
                            'name': 'data_conflict',
                            'action': 'register',
                            'register': False
                        }
                        }), 400

    if not validate_username(username):
        return jsonify({'msg': 'Invalid username',
                        'status': {
                            'name': 'invalid_data',
                            'action': 'register',
                            'register': False
                        }
                        }), 400

    user = {'username': username,
            'password_hash': get_password(password),
            'email': email,
            'books_owned': 0,
            'followers': 0,
            'following': 0,
            'about': 'New account',
            'admin': False,
            'profile_image': 'default.jpg',
            'created_at': datetime.datetime.utcnow(),
            }

    mongo.db.users.insert_one(user)

    return jsonify({'msg': 'User created succesfully',
                    'status': {
                        'name': 'created',
                        'action': 'register',
                        'register': True
                    }
                    }), 201
