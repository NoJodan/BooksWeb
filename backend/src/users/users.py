from flask import request, jsonify, blueprints
from app import mongo, app
import app as application
from utils.passwords import check_password, get_password
from utils.users import validate_username, validate_user
import datetime
from flask_jwt_extended import create_access_token 

users_blueprint = blueprints.Blueprint('users', __name__)



@users_blueprint.route('/users/login')
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
                        'status':{
                            'name': 'not_found',
                            'action': 'login',
                            'login': False
                        }
                        }), 401

    if auth and check_password(auth.password,user['password_hash']):
        token = create_access_token(identity=auth.username,expires_delta=expires_delta)

        return jsonify({'msg': 'User logged in successfully',
                        'status':{
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

@users_blueprint.route('/users/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    
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
    
    mongo.db.users.insert_one({'username': username,
                               'password_hash': get_password(password),
                               'admin': False,
                               'created_at': datetime.datetime.utcnow(),
                               })
    
    return jsonify({'msg': 'User created succesfully', 
                    'status': {
                        'name': 'created',
                        'action': 'register',
                        'register': True
                    }
                    }), 201


