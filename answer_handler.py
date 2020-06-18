from flask import render_template, request, redirect, Blueprint, abort, session
import data_manager
import util

answer = Blueprint('answer', __name__, template_folder='templates')


@answer.route("/question/<question_id>/new-answer", methods=["POST", "GET"])
def add_answer(question_id):
    if 'username' not in session:
        abort(401)
    username = session['username']
    user_id = session['user_id']
    new_record = {"question_id": str(question_id)}
    if request.method == "POST":
        new_record = get_answer_data(new_record)
        data_manager.add_record(new_record, "answer")
        return redirect("/question/" + str(question_id))
    return render_template(
        "answer_form.html",
        old_record=new_record,
        is_new=True,
        user_id=user_id,
        username=username
    )


@answer.route("/answer/<answer_id>/edit", methods=["POST", "GET"])
def edit_answer(answer_id):
    if 'username' not in session:
        abort(401)
    username = session['username']
    user_id = data_manager.get_user_id(username)['id']
    old_record = data_manager.get_specific_record(answer_id, "answer")
    if user_id != old_record["user_id"]:
        abort(401)
    if request.method == "POST":
        old_record = get_answer_data(old_record)
        data_manager.edit_record(old_record, "answer")
        return redirect("/question/" + str(old_record["question_id"]))
    return render_template(
        "answer_form.html",
        old_record=old_record,
        is_new=False,
        user_id=user_id,
        username=username
    )


@answer.route("/answer/<answer_id>/delete")
def delete_answer(answer_id):
    if 'username' not in session:
        abort(401)
    username = session['username']
    user_id = data_manager.get_user_id(username)['id']
    old_record = data_manager.get_specific_record(answer_id, "answer")
    if user_id != old_record["user_id"]:
        abort(401)
    data_manager.delete_connected_comment(None, answer_id)
    data_manager.delete_record(answer_id, "answer")
    return redirect("/question/" + str(old_record["question_id"]))


def get_answer_data(record):
    record["submission_time"] = util.get_new_timestamp()
    record["message"] = request.form["description"]
    record["user_id"] = data_manager.get_user_id(session['username'])['id']
    if 'file' in request.files:
        file = request.files['file']
        record["image"] = util.save_image(file, data_manager.UPLOAD_FOLDER, "answer", str(record["question_id"]))
    if not record["image"]:
        record["image"] = ""
    return record


@answer.route("/answer/<answer_id>/status")
def add_answer_status(answer_id):
    answer_data = data_manager.get_specific_record(answer_id, "answer")
    question_owner_id = data_manager.get_question_owner_based_on_answer(answer_id)['user_id']
    if 'username' in session and int(question_owner_id) == int(data_manager.get_user_id(session['username'])['id']):
        status = not answer_data["accepted"]
        data_manager.change_answer_status(answer_id, status)
        return redirect("/question/" + str(answer_data["question_id"]))
    else:
        abort(401)
