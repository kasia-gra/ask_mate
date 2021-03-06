from flask import render_template, Blueprint, abort, session

import util
from controllers import data_manager

user = Blueprint('user', __name__, 'templates')


@user.route("/users")
def list_users():
    if 'username' not in session:
        abort(401)
    else:
        username, logged_user_id = util.set_user_details_based_on_logged_status()
        users = data_manager.get_users()
    return render_template(
        "users_list.html",
        user_id=logged_user_id,
        username=username,
        users=users
        )


@user.route("/user/<user_id>")
def show_user(user_id):
    if 'username' not in session:
        abort(401)
    else:
        username, logged_user_id = util.set_user_details_based_on_logged_status()
        user_details = data_manager.get_user_by_id(int(user_id))
        questions = data_manager.get_data_from_user_by_option(int(user_id), 'question')
        questions = util.prepare_questions_to_display(questions)
        answers = data_manager.get_data_from_user_by_option(int(user_id), 'answer')
        answers = util.prepare_message_to_display(answers)
        comments = data_manager.get_data_from_user_by_option(int(user_id), 'comment')
        comments = util.prepare_message_to_display(comments)
    return render_template(
        "user_details.html",
        user_id=logged_user_id,
        username=username,
        user=user_details,
        questions=questions,
        answers=answers,
        comments=comments
        )
