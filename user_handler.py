from flask import render_template, request, redirect, url_for, Blueprint, flash


user = Blueprint('user', __name__, 'templates')


@user.route("/users")
def list_users():
    
    return render_template("users_list.html")
