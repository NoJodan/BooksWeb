import cerberus

local_book_schema = {
    'name': {'type': 'string', 'required': True},
    'description': {'type': 'string', 'required': True},
    'author': {'type': 'string', 'required': True},
    'categories': {'type': 'list', 'minlength': 1, 'schema': {'type': 'string'}, 'required': True},
}

provided_book_schema = local_book_schema.copy()
provided_book_schema.pop('author')

def validate_local_book(book):
    return cerberus.Validator(local_book_schema).validate(book)

def validate_provided_book(book):
    return cerberus.Validator(provided_book_schema).validate(book)