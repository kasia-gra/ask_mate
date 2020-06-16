from flask import render_template, request, redirect, url_for, Blueprint, flash, session
import bcrypt
import data_manager
import session_handler
import util

registration = Blueprint('registration', __name__, template_folder='templates')


@registration.route("/login", methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect("/")
    if request.method == "POST":
        username = request.form.get("email")
        password = request.form.get("password")
        hashed_password = data_manager.get_password(username)["password"]
        print(hashed_password)
        if password and bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            session["username"] = username
            session["user_id"] = data_manager.get_user_id(username)["id"]
            return redirect("/")
        flash('Wrong password!')
        return redirect("/register")
    return render_template("login.html")


@registration.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        if request.form.get("password") == request.form.get("cpassword"):
            user_dict = {}
            user_dict["email"] = request.form.get("email")
            user_dict["password"] = bcrypt.hashpw(request.form.get("password").encode("utf-8"),
                                                  bcrypt.gensalt(rounds=10))
            user_dict["registration_time"] = util.get_new_timestamp()
            user_dict["reputation"] = 0
            data_manager.add_user(user_dict)
        else:
            flash('Passwords not matching - try again')
            return redirect("/register")
        return redirect("/")
    return render_template("register.html")


@registration.route("/logout")
def logout():
    if 'username' in session_handler:
        session.pop('username', None)
        session.pop('user_id', None)
    return redirect("/")
