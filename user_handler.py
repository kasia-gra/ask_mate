from flask import render_template, request, redirect, url_for, Blueprint, flash, session


user = Blueprint('user', __name__, 'templates')


@user.route("/users")
def list_users():
    if 'username' not in session:
        flash("You can't see users!")
        return redirect("/")
    else:
        logged_status = True
        username = session['username']
        user_id = session['user_id']
    return render_template(
        "users_list.html",
        logged=logged_status,
        user_id=user_id,
        username=username
        )
