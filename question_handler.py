from flask import render_template, request, redirect, Blueprint, flash, session, abort
import data_manager
import util

question = Blueprint('question', __name__, template_folder='templates')


@question.route("/question", methods=["POST", "GET"])
def add_question():
    if 'username' not in session:
        abort(401)
    username = session['username']
    user_id = session['user_id']
    new_record = {}
    if request.method == "POST":
        new_record = get_question_data(new_record)
        data_manager.add_record(new_record, "question")
        return redirect("/list")
    return render_template(
        "question_form.html",
        old_record=new_record,
        is_new=True,
        user_id=user_id,
        username=username
    )


@question.route("/question/<question_id>/edit", methods=["POST", "GET"])
def edit_question(question_id):
    if 'username' not in session:
        abort(401)
    username = session['username']
    old_record = data_manager.get_specific_record(question_id, "question")
    user_id = data_manager.get_user_id(username)
    if user_id != old_record["user_id"]:
        abort(401)
    if request.method == "POST":
        old_record = get_question_data(old_record)
        data_manager.edit_record(old_record, "question")
        return redirect("/question/" + str(question_id))
    return render_template(
        "question_form.html",
        old_record=old_record,
        is_new=False,
        user_id=user_id,
        username=username
    )


@question.route("/question/<question_id>/delete")
def delete_question(question_id):
    if 'username' not in session:
        abort(401)
    username = session['username']
    user_id = data_manager.get_user_id(username)
    record = data_manager.get_specific_record(question_id, "question")
    if user_id != record["user_id"]:
        abort(401)
    all_answers = data_manager.get_all_records("answer")
    for answer in all_answers:
        if str(answer.get("question_id")) == str(question_id):
            data_manager.delete_record(answer.get("id"), "answer")
            data_manager.delete_connected_comment(-1, answer.get("id"))
    data_manager.delete_connected_comment(question_id, -1)
    data_manager.delete_connected_tags(question_id)
    data_manager.delete_record(question_id, "question")
    return redirect("/list")


def get_question_data(record):
    record["title"] = request.form["title"]
    record["submission_time"] = util.get_new_timestamp()
    record["message"] = request.form["description"]
    record["user_id"] = data_manager.get_user_id(session['username'])['id']
    if 'file' in request.files:
        file = request.files['file']
        record["image"] = util.save_image(file, data_manager.UPLOAD_FOLDER, "question")
    if not record["image"]:
        record["image"] = ""
    return record
