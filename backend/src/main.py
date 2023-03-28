from app import app
from books.books import books_blueprint
from users.users import users_blueprint
from others.others import others_blueprint

app.register_blueprint(books_blueprint, url_prefix='/api')
app.register_blueprint(users_blueprint, url_prefix='/api')
app.register_blueprint(others_blueprint, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True,port=8000)