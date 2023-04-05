from app import mongo, app
import hashlib, datetime
from werkzeug.utils import secure_filename
import base64
import os

PROFILE_IMAGES_PATH = app.config['USERS_PROFILE_IMAGES_PATH']
ALLOWED_EXTENSIONS_USERSIMG = app.config['ALLOWED_EXTENSIONS_USERSIMG']

def delete_profile_image(file_name):
    os.remove(f'{PROFILE_IMAGES_PATH}/{file_name}')

def validate_category(category):
    return True if mongo.db.categories.find_one({'name': category}) else False

def get_file_name(data):
    return hashlib.sha256(hashlib.sha256(data).hexdigest().encode() + str(datetime.datetime.utcnow()).encode()).hexdigest()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_USERSIMG

def process_profile_image(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(os.getcwd() + app.config['USERS_PROFILE_IMAGES_PATH'], filename))
        return filename
    
def send_profile_image(name):
    with open(f'{os.getcwd()}{PROFILE_IMAGES_PATH}/{name}', 'rb') as img_file:
        image_bytes = img_file.read()
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    return image_base64