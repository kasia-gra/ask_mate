from flask import render_template, request, redirect, url_for, Blueprint, session
from controllers import data_manager
import util

comment = Blueprint('comment', __name__, template_folder='templates')


@comment.route("/question/<int:question_id>/new-comment", methods=["POST", "GET"])
def comment_question(question_id):
    util.check_if_user_is_logged()
    username, logged_user_id = util.get_user_details_from_session()
    new_comment_to_question = {"question_id": question_id}
    if request.method == "POST":
        new_comment_to_question["answer_id"] = None
        add_comment_to_database(new_comment_to_question)
        return redirect(url_for("show_question", question_id=str(question_id)))
    return render_template(
        "forms/../templates/comment_form.html",
        question_id=str(question_id),
        user_id=logged_user_id,
        username=username
    )


@comment.route("/answer/<int:answer_id>/new-comment", methods=["POST", "GET"])
def comment_answer(answer_id):
    util.check_if_user_is_logged()
    username, logged_user_id = util.get_user_details_from_session()
    answer = data_manager.get_specific_record(answer_id, "answer")
    question_id = answer["question_id"]
    new_comment_to_answer = {"answer_id": answer_id}
    if request.method == "POST":
        new_comment_to_answer["question_id"] = None
        add_comment_to_database(new_comment_to_answer)
        return redirect(url_for("show_question", question_id=str(question_id)))
    return render_template(
        "forms/../templates/comment_form.html",
        answer_id=answer_id,
        question_id=question_id,
        user_id=logged_user_id,
        username=username
    )


@comment.route("/comment/<int:comment_id>/edit", methods=["POST", "GET"])
def edit_comment(comment_id):
    util.check_if_user_is_logged()
    username, logged_user_id = util.get_user_details_from_session()
    selected_comment = data_manager.get_specific_record(comment_id, "comment")
    util.check_if_user_is_owner(logged_user_id, selected_comment["user_id"])
    if request.method == "POST":
        selected_comment["message"] = request.form["message"]
        selected_comment["edited_number"] = selected_comment["edited_number"] + 1 if selected_comment[
                                                                                         "edited_number"] is not None else 1
        selected_comment["submission_time"] = util.get_new_timestamp()
        data_manager.edit_comment(selected_comment)
        question_id = selected_comment["question_id"] if type(
            selected_comment["question_id"]) is int else data_manager.get_specific_record(
            selected_comment.get("answer_id"),
            "answer").get("question_id")
        return redirect(url_for("show_question", question_id=question_id))
    return render_template(
        "forms/../templates/comment_form.html",
        comment=selected_comment,
        user_id=logged_user_id,
        username=username
    )


@comment.route("/comments/<int:comment_id>/delete")
def delete_comment(comment_id):
    util.check_if_user_is_logged()
    username, logged_user_id = util.get_user_details_from_session()
    selected_comment = data_manager.get_specific_record(comment_id, "comment")
    util.check_if_user_is_owner(logged_user_id, selected_comment["user_id"])
    if type(selected_comment.get("question_id")) is int:
        question_id = selected_comment.get("question_id")
    else:
        answer_id = selected_comment.get("answer_id")
        answer = data_manager.get_specific_record(answer_id, "answer")
        question_id = answer.get("question_id")
    data_manager.delete_record(comment_id, 'comment')
    return redirect(url_for("show_question", question_id=question_id))


def add_comment_to_database(record):
    record["message"] = request.form["message"]
    record["edited_number"] = 0
    record["submission_time"] = util.get_new_timestamp()
    record["user_id"] = data_manager.get_user_data(session['username'])['id']
    data_manager.add_comment(record)
