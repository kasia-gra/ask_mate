from flask import render_template, request, redirect, url_for, Blueprint, flash, session
import bcrypt
import data_manager
import util

registration = Blueprint('registration', __name__, template_folder='templates')


@registration.route("/login", methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect("/")
    if request.method == "POST":
        username = request.form.get("email")
        if not user_already_registered(username):
            flash('Wrong password or username!')
            return redirect("/login")
        password = request.form.get("password")
        if username and password:
            hashed_password = data_manager.get_user_data(username).get("password")
            if bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8")):
                session["username"] = username
                session["user_id"] = data_manager.get_user_id(username).get("id")
                return redirect("/")
        flash('Wrong password or username!')
        return redirect("/login")
    return render_template("login.html", logged=False)


def user_already_registered(email):
    for user in data_manager.get_all_users_emails():
        if user['email'] == email:
            return True
    return False


@registration.route("/registration", methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect("/")
    if request.method == "POST":
        if user_already_registered(request.form.get("email")):
            flash('User already registered !')
            return redirect("/registration")
        elif request.form.get("password") != request.form.get("cpassword"):
            flash('Passwords not matching - try again')
            return redirect("/registration")
        else:
            user_dict = {}
            user_dict["email"] = request.form.get("email")
            user_dict["password"] = bcrypt.hashpw(request.form.get("password").encode("utf-8"),
                                                  bcrypt.gensalt(rounds=10)).decode("utf-8")
            user_dict["registration_time"] = util.get_new_timestamp()
            user_dict["reputation"] = 0
            data_manager.add_user(user_dict)
            flash('Congratulations - you have registered successfully - you can now log in')
            return redirect("/login")
    return render_template("register.html", logged=False)


@registration.route("/logout")
def logout():
    if 'username' in session:
        session.pop('username', None)
        session.pop('user_id', None)
    return redirect("/")
