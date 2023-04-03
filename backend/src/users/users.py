import base64
from flask import request, jsonify, blueprints
from app import mongo, app
from flask_pymongo import ObjectId
from utils.others import process_profile_image, delete_profile_image
from utils.passwords import check_password, get_password
from utils.users import validate_username, validate_user, get_username, validate_user_by_id, get_user_id, validate_admin
from flask_jwt_extended import jwt_required
from utils.decorators import user_access_required
import datetime
from flask_jwt_extended import create_access_token
from schemas.users import validate_user as validate_user_schema

users_blueprint = blueprints.Blueprint('users', __name__)
PROFILE_IMAGES_PATH = app.config['USERS_PROFILE_IMAGES_PATH']


@users_blueprint.route('/users/username/<username>', methods=['GET'])
def get_user_data(username):
    user_id = get_user_id(username)


@users_blueprint.route('/users/<user>', methods=['DELETE'])
@jwt_required()
@user_access_required('delete', 'not_deleted', pass_user_id=True)
def delete_user(user, user_id):
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
def update_user(user_id):
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
    profile_image = request.json.get('profile_image')

    if not username or not password:
        return jsonify({'msg': 'Username or password missing',
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
            'admin': False,
            'created_at': datetime.datetime.utcnow(),
            }

    if profile_image:
        user['photo_image'] = process_profile_image(profile_image)

    mongo.db.users.insert_one(user)

    return jsonify({'msg': 'User created succesfully',
                    'status': {
                        'name': 'created',
                        'action': 'register',
                        'register': True
                    }
                    }), 201
