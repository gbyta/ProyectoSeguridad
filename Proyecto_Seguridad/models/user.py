from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Diccionario global para simular la base de datos en memoria
users_db = {}

class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = str(id)
        self.username = username
        self.password_hash = password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_id(user_id):
        return users_db.get(str(user_id))

    @staticmethod
    def get_by_username(username):
        for user in users_db.values():
            if user.username == username:
                return user
        return None

    @staticmethod
    def create(username, password):
        user_id = str(len(users_db) + 1)
        password_hash = generate_password_hash(password)
        new_user = User(user_id, username, password_hash)
        users_db[user_id] = new_user
        return new_user