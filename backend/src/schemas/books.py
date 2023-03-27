import cerberus

schema = {
    'name': {'type': 'string', 'required': True},
    'description': {'type': 'string', 'required': True},
    'author': {'type': 'string', 'required': True},
    'categories': {'type': 'list', 'minlength': 1, 'schema': {'type': 'string'}, 'required': True},
}

def validate_book(book):
    return cerberus.Validator(schema).validate(book)