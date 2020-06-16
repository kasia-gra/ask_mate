from flask import render_template, request, redirect, url_for, Blueprint, flash
import bcrypt
import data_manager
import util

registration = Blueprint('registration', __name__, template_folder='templates')


@registration.route("/registration", methods=['GET', 'POST'])
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
            return redirect("/registration")
        return redirect("/")
    return render_template("register.html")
