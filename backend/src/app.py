from flask import Flask, request, jsonify
import datetime
from flask_pymongo import PyMongo
from flask_cors import CORS
from dotenv import load_dotenv
from os import getenv
from flask_jwt_extended import JWTManager
load_dotenv()

app = Flask(__name__)
app.config['MONGO_URI'] = getenv('MONGO_URI')
app.config['SECRET_KEY'] = getenv('SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=30)
mongo = PyMongo(app)
jwt = JWTManager(app)
CORS(app)
