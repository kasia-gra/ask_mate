from flask import render_template, Blueprint, abort, session


user = Blueprint('user', __name__, 'templates')


@user.route("/users")
def list_users():
    if 'username' not in session:
        abort(401)
    else:
        username = session['username']
        user_id = session['user_id']
    return render_template(
        "users_list.html",
        user_id=user_id,
        username=username
        )
