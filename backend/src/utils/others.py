from app import mongo, app
import hashlib, datetime
import base64
import os

PROFILE_IMAGES_PATH = app.config['USERS_PROFILE_IMAGES_PATH']

def delete_profile_image(file_name):
    os.remove(f'{PROFILE_IMAGES_PATH}/{file_name}')

def validate_category(category):
    return True if mongo.db.categories.find_one({'name': category}) else False

def get_file_name(data):
    return hashlib.sha256(hashlib.sha256(data).hexdigest().encode() + str(datetime.datetime.utcnow()).encode()).hexdigest()

def process_profile_image(data):
    photo_bytes = base64.b64decode(data)
    photo_name = get_file_name(photo_bytes) + '.jpg'
    with open(f'{PROFILE_IMAGES_PATH}/{photo_name}', 'wb') as f:
        f.write(photo_bytes)
    return photo_name