from flask import render_template, request, redirect, Blueprint, flash, session, abort
import data_manager
import util

question = Blueprint('question', __name__, template_folder='templates')


@question.route("/question", methods=["POST", "GET"])
def add_question():
    util.check_if_user_is_logged()
    username, logged_user_id = util.get_user_details_from_session()
    default_blank_question = {}
    if request.method == "POST":
        new_question = set_question_values(default_blank_question)
        data_manager.add_record(new_question, "question")
        return redirect("/list")
    return render_template(
        "question_form.html",
        old_record=default_blank_question,
        is_new=True,
        user_id=logged_user_id,
        username=username
    )


@question.route("/question/<question_id>/edit", methods=["POST", "GET"])
def edit_question(question_id):
    util.check_if_user_is_logged()
    username, logged_user_id = util.get_user_details_from_session()
    selected_question = data_manager.get_specific_record(question_id, "question")
    util.check_if_user_is_owner(logged_user_id, selected_question["user_id"])
    if request.method == "POST":
        updated_question = set_question_values(selected_question)
        data_manager.edit_record(updated_question, "question")
        return redirect("/question/" + str(question_id))
    return render_template(
        "question_form.html",
        old_record=selected_question,
        is_new=False,
        user_id=logged_user_id,
        username=username
    )


@question.route("/question/<question_id>/delete")
def delete_question(question_id):
    util.check_if_user_is_logged()
    username, logged_user_id = util.get_user_details_from_session()
    selected_question = data_manager.get_specific_record(question_id, "question")
    util.check_if_user_is_owner(logged_user_id, selected_question["user_id"])
    all_answers = data_manager.get_all_records("answer")
    for answer in all_answers:
        if str(answer.get("question_id")) == str(question_id):
            data_manager.delete_record(answer.get("id"), "answer")
            data_manager.delete_connected_comment(-1, answer.get("id"))
    data_manager.delete_connected_comment(question_id, -1)
    data_manager.delete_connected_tags(question_id)
    data_manager.delete_record(question_id, "question")
    return redirect("/list")


def set_question_values(manipulated_question):
    manipulated_question["title"] = request.form["title"]
    manipulated_question["submission_time"] = util.get_new_timestamp()
    manipulated_question["message"] = request.form["description"]
    manipulated_question["user_id"] = data_manager.get_user_id(session['username'])['id']
    if 'file' in request.files:
        file = request.files['file']
        manipulated_question["image"] = util.save_image(file, data_manager.UPLOAD_FOLDER, "question")
    if not manipulated_question["image"]:
        manipulated_question["image"] = ''
    return manipulated_question
