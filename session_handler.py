from flask import session
import data_manager
import bcrypt


def create_session(email):
    session["username"] = email
    session["user_id"] = data_manager.get_user_id(email)["id"]


def drop_session():
    session.pop('username', None)
    session.pop('user_id', None)


def validate_password_match(email, password):
    if bcrypt.checkpw(bytes(password, "UTF-8"), bytes(data_manager.get_password_from_user(email)["password"], "UTF-8")):
        return True
    return False


def hash_password(password):
    return bcrypt.hashpw(password, bcrypt.gensalt())
