from flask import Blueprint, jsonify, request
from app import mongo
from flask_pymongo import ObjectId
from flask_jwt_extended import jwt_required, get_jwt_identity, decode_token
from utils.users import get_user_id, get_username, validate_admin
import time

others_blueprint = Blueprint('others', __name__)

@others_blueprint.route('/others/check-jwt', methods = ['GET'])
def check_jwt():
    
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'msg': 'No token provided','status': {
            'name': 'not_found',
            'action': 'check',
            'check': False
        }})
    token = token.replace('Bearer ', '')
    
    decoded_token = decode_token(token,allow_expired=True)
    is_expired =  decoded_token.get('exp') < time.time()
    
    
    
    return jsonify({'msg': 'JWT is valid','status': {
        'name': 'valid',
        'action': 'check',
        'check': True
        },
        'data': {
            'is_expired': is_expired
    }})