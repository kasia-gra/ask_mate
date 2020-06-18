from flask import render_template, request, redirect, Blueprint, abort, session
from controllers import data_manager
import util

answer = Blueprint('answer', __name__, template_folder='templates')


@answer.route("/question/<question_id>/new-answer", methods=["POST", "GET"])
def add_answer(question_id):
    util.check_if_user_is_logged()
    username, logged_user_id = util.get_user_details_from_session()
    default_blank_answer = {"question_id": str(question_id)}
    if request.method == "POST":
        new_answer = set_answer_values(default_blank_answer)
        if not new_answer["image"]:
            new_answer["image"] = ''
        data_manager.add_record(new_answer, "answer")
        return redirect("/question/" + str(question_id))
    return render_template(
        "answer_form.html",
        old_record=default_blank_answer,
        is_new=True,
        user_id=logged_user_id,
        username=username
    )


@answer.route("/answer/<answer_id>/edit", methods=["POST", "GET"])
def edit_answer(answer_id):
    util.check_if_user_is_logged()
    username, logged_user_id = util.get_user_details_from_session()
    selected_answer = data_manager.get_specific_record(answer_id, "answer")
    util.check_if_user_is_owner(logged_user_id, selected_answer["user_id"])
    if request.method == "POST":
        old_record = set_answer_values(selected_answer)
        if not old_record["image"]:
            old_record["image"] = ''
        data_manager.edit_record(old_record, "answer")
        return redirect("/question/" + str(old_record["question_id"]))
    return render_template(
        "answer_form.html",
        old_record=selected_answer,
        is_new=False,
        user_id=logged_user_id,
        username=username
    )


@answer.route("/answer/<answer_id>/delete")
def delete_answer(answer_id):
    util.check_if_user_is_logged()
    username, logged_user_id = util.get_user_details_from_session()
    selected_answer = data_manager.get_specific_record(answer_id, "answer")
    util.check_if_user_is_owner(logged_user_id, selected_answer["user_id"])
    data_manager.delete_connected_comment(None, answer_id)
    data_manager.delete_record(answer_id, "answer")
    return redirect("/question/" + str(selected_answer["question_id"]))


def set_answer_values(manipulated_answer):
    manipulated_answer["submission_time"] = util.get_new_timestamp()
    manipulated_answer["message"] = request.form["description"]
    manipulated_answer["user_id"] = data_manager.get_user_data(session['username'])['id']
    if 'file' in request.files:
        file = request.files['file']
        manipulated_answer["image"] = util.save_image(file, data_manager.UPLOAD_FOLDER, "answer", str(manipulated_answer["question_id"]))
    return manipulated_answer


@answer.route("/answer/<answer_id>/status")
def add_answer_status(answer_id):
    answer_data = data_manager.get_specific_record(answer_id, "answer")
    answer_owner = answer_data['user_id']
    reputation_points_based_on_accept_status = {True: 15, False: -15}
    question_owner_id = data_manager.get_question_owner_based_on_answer(answer_id)['user_id']
    if 'username' in session and int(question_owner_id) == int(data_manager.get_user_data(session['username'])['id']):
        status = not answer_data["accepted"]
        data_manager.change_answer_status(answer_id, status)
        data_manager.update_reputation(answer_owner, reputation_points_based_on_accept_status[status])
        return redirect("/question/" + str(answer_data["question_id"]))
    return abort(401)
