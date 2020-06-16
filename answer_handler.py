from flask import render_template, request, redirect, Blueprint, flash, session
import data_manager
import util

answer = Blueprint('answer', __name__, template_folder='templates')


@answer.route("/question/<question_id>/new-answer", methods=["POST", "GET"])
def add_answer(question_id):
    if 'username' not in session:
        flash("You can't add answer!")
        return redirect("/question/" + str(question_id))
    logged_status = True
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
        logged=logged_status,
        user_id=user_id,
        username=username
    )


@answer.route("/answer/<answer_id>/edit", methods=["POST", "GET"])
def edit_answer(answer_id):
    old_record = data_manager.get_specific_record(answer_id, "answer")
    if 'username' not in session:
        flash("You can't edit answer!")
        return redirect("/question/" + str(old_record["question_id"]))
    logged_status = True
    username = session['username']
    user_id = session['user_id']
    if request.method == "POST":
        old_record = get_answer_data(old_record)
        data_manager.edit_record(old_record, "answer")
        return redirect("/question/" + str(old_record["question_id"]))
    return render_template(
        "answer_form.html",
        old_record=old_record,
        is_new=False,
        logged=logged_status,
        user_id=user_id,
        username=username
    )


@answer.route("/answer/<answer_id>/delete")
def delete_answer(answer_id):
    old_record = data_manager.get_specific_record(answer_id, "answer")
    if 'username' not in session:
        flash("You can't delete answer!")
        return redirect("/question/" + str(old_record["question_id"]))
    data_manager.delete_connected_comment(None, answer_id)
    data_manager.delete_record(answer_id, "answer")
    return redirect("/question/" + str(old_record["question_id"]))


def get_answer_data(record):
    record["submission_time"] = util.get_new_timestamp()
    record["message"] = request.form["description"]
    if 'file' in request.files:
        file = request.files['file']
        record["image"] = util.save_image(file, data_manager.UPLOAD_FOLDER, "answer", str(record["question_id"]))
    if not record["image"]:
        record["image"] = ""
    return record
