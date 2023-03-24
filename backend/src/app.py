from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/booksweb'
mongo = PyMongo(app)

CORS(app)

db = mongo.db.books

@app.route('/books', methods = ['POST'])
def createBook():
    id = db.insert_one({
        'name': request.json['name'],
        'description': request.json['description'],
        'autor': request.json['autor']
    })
    return jsonify(str(id.inserted_id))

@app.route('/books', methods = ['GET'])
def getBooks():
    books = []
    for book in db.find():
        books.append({
            '_id': str(ObjectId(book['_id'])),
            'name': book['name'],
            'description': book['description'],
            'autor': book['autor']
        })
    return jsonify(books)

@app.route('/book/<id>', methods = ['GET'])
def getBook(id):
    book = db.find_one({'_id': ObjectId(id)})
    return jsonify({
            '_id': str(ObjectId(book['_id'])),
            'name': book['name'],
            'description': book['description'],
            'autor': book['autor']
    })

@app.route('/book/<id>', methods = ['DELETE'])
def deleteBook(id):
    db.delete_one({'_id': ObjectId(id)})
    return jsonify({'msg': 'Book deleted'})

@app.route('/book/<id>', methods = ['PUT'])
def updateBook(id):
    db.update_one({'_id': ObjectId(id)}, {'$set': {
        'name': request.json['name'],
        'description': request.json['description'],
        'autor': request.json['autor']
    }})
    return jsonify({'msg': 'Book updated'})

if __name__ == "__main__":
    app.run(debug = True)