import cerberus

schema = {
    'username': {'type': 'string', 'required': False},
    'password': {'type': 'string', 'required': False},
    'admin': {'type': 'boolean', 'required': False},
    'profile_image': {'type': 'string', 'required': False},
}

def validate_user(user):
    return cerberus.Validator(schema).validate(user)
