from flask import render_template, Blueprint, abort, session

import data_manager, util

user = Blueprint('user', __name__, 'templates')


@user.route("/users")
def list_users():
    if 'username' not in session:
        abort(401)
    else:
        username = session['username']
        user_id = data_manager.get_user_id(username)['id']
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
        logged_user_id = data_manager.get_user_id(username)['id']
        user_details = data_manager.get_user_by_id(int(user_id))
        questions = data_manager.get_questions_by_user_id(int(user_id))
        questions = util.prepare_questions_to_display(questions)
        answers = data_manager.get_answers_by_user_id(int(user_id))
        answers = util.prepare_message_to_display(answers)
        comments = data_manager.get_comments_by_user_id(int(user_id))
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
