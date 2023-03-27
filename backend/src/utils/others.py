from app import mongo


def validate_category(category):
    return True if mongo.db.categories.find_one({'name': category}) else False