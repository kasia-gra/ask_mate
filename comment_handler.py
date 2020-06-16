from flask import render_template, request, redirect, url_for, Blueprint, flash, session
import data_manager
import util

comment = Blueprint('comment', __name__, template_folder='templates')


@comment.route("/question/<int:question_id>/new-comment", methods=["POST", "GET"])
def comment_question(question_id):
    if 'username' not in session:
        flash("You can't add comment!")
        return redirect(url_for("show_question", question_id=str(question_id)))
    logged_status = True
    username = session['username']
    user_id = session['user_id']
    new_record = {"question_id": question_id}
    if request.method == "POST":
        new_record["answer_id"] = None
        add_comment_to_database(new_record)
        return redirect(url_for("show_question", question_id=str(question_id)))
    return render_template(
        "comment_form.html",
        question_id=str(question_id),
        logged=logged_status,
        user_id=user_id,
        username=username
    )


@comment.route("/answer/<int:answer_id>/new-comment", methods=["POST", "GET"])
def comment_answer(answer_id):
    answer = data_manager.get_specific_record(answer_id, "answer")
    question_id = answer["question_id"]
    if 'username' not in session:
        flash("You can't add comment!")
        return redirect(url_for("show_question", question_id=str(question_id)))
    logged_status = True
    username = session['username']
    user_id = session['user_id']
    new_record = {"answer_id": answer_id}
    if request.method == "POST":
        new_record["question_id"] = None
        add_comment_to_database(new_record)
        return redirect(url_for("show_question", question_id=str(question_id)))
    return render_template(
        "comment_form.html",
        answer_id=answer_id,
        question_id=question_id,
        logged=logged_status,
        user_id=user_id,
        username=username
    )


@comment.route("/comment/<int:comment_id>/edit", methods=["POST", "GET"])
def edit_comment(comment_id):
    comment = data_manager.get_specific_record(comment_id, "comment")
    if 'username' not in session:
        flash("You can't edit comment!")
        return redirect(url_for("show_question", question_id=comment["question_id"]))
    logged_status = True
    username = session['username']
    user_id = session['user_id']
    if request.method == "POST":
        comment["message"] = request.form["message"]
        comment["edited_number"] = comment["edited_number"] + 1 if comment["edited_number"] is not None else 1
        comment["submission_time"] = util.get_new_timestamp()
        data_manager.edit_comment(comment)
        question_id = comment["question_id"] if type(
            comment["question_id"]) is int else data_manager.get_specific_record(comment.get("answer_id"),
                                                                                 "answer").get("question_id")
        return redirect(url_for("show_question", question_id=question_id))
    return render_template(
        "comment_form.html",
        comment=comment,
        logged=logged_status,
        user_id=user_id,
        username=username
    )


@comment.route("/comments/<int:comment_id>/delete")
def delete_comment(comment_id):
    comment = data_manager.get_specific_record(comment_id, "comment")
    if type(comment.get("question_id")) is int:
        question_id = comment.get("question_id")
    else:
        answer_id = comment.get("answer_id")
        answer = data_manager.get_specific_record(answer_id, "answer")
        question_id = answer.get("question_id")
    if 'username' not in session:
        flash("You can't delete answer!")
        return redirect(url_for("show_question", question_id=question_id))
    data_manager.delete_comment(comment_id)
    return redirect(url_for("show_question", question_id=question_id))


def add_comment_to_database(record):
    record["message"] = request.form["message"]
    record["edited_number"] = 0
    record["submission_time"] = util.get_new_timestamp()
    data_manager.add_comment(record)
