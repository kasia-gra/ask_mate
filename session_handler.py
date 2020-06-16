from flask import session
import data_manager
import bcrypt


session.secret_key = "$2a$10$vI8aWBnW3fID.ZQ4/zo1G.q1lRps.9cGLcZEiGDMVr5yUP1KUYTa"


def create_session(email):
    session["username"] = email


def drop_session():
    session.pop('username', None)


def validate_password_match(email, password):
    if bcrypt.checkpw(bytes(password, "UTF-8"), bytes(data_manager.get_password_from_user(email)["password"], "UTF-8")):
        return True
    return False


def hash_password(password):
    return bcrypt.hashpw(password, bcrypt.gensalt())
