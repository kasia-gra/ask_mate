from flask import render_template, Blueprint, abort, session

import data_manager

user = Blueprint('user', __name__, 'templates')


@user.route("/users")
def list_users():
    if 'username' not in session:
        abort(401)
    else:
        username = session['username']
        user_id = session['user_id']
        users = data_manager.get_users()
    return render_template(
        "users_list.html",
        user_id=user_id,
        username=username,
        users=users
        )


@user.route("/user/<user_id>")
def show_user(user_id):
    if 'username' not in session:
        abort(401)
    else:
        username = session['username']
        logged_user_id = session['user_id']
        user_details = data_manager.get_user_by_id(int(user_id))
    return render_template(
        "user_details.html",
        user_id=logged_user_id,
        username=username,
        user=user_details
        )


