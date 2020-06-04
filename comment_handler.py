from flask import render_template, request, redirect, url_for, Blueprint
import data_manager
import util

comment = Blueprint('comment', __name__, template_folder='templates')


@comment.route("/question/<int:question_id>/new-comment", methods=["POST", "GET"])
def comment_question(question_id):
    new_record = {"question_id": question_id}
    if request.method == "POST":
        new_record["answer_id"] = None
        add_comment_to_database(new_record)
        return redirect(url_for("show_question", question_id=str(question_id)))
    return render_template("comment_form.html", question_id=str(question_id))


@comment.route("/answer/<int:answer_id>/new-comment", methods=["POST", "GET"])
def comment_answer(answer_id):
    answer = data_manager.get_specific_record(answer_id, "answer")
    question_id = answer["question_id"]
    new_record = {"answer_id": answer_id}
    if request.method == "POST":
        new_record["question_id"] = None
        add_comment_to_database(new_record)
        return redirect(url_for("show_question", question_id=str(question_id)))
    return render_template("comment_form.html", answer_id=answer_id, question_id=question_id)


@comment.route("/comment/<int:comment_id>/edit", methods=["POST", "GET"])
def edit_comment(comment_id):
    element = data_manager.get_specific_record(comment_id, "comment")
    if request.method == "POST":
        element["message"] = request.form["message"]
        element["edited_number"] = element["edited_number"] + 1 if element["edited_number"] is not None else 1
        element["submission_time"] = util.get_new_timestamp()
        data_manager.edit_comment(element)
        if comment["question_id"]:
            question_id = element["question_id"]
        else:
            data_manager.get_specific_record(element.get("answer_id"), "answer").get("question_id")
        return redirect(url_for("show_question", question_id=question_id))
    return render_template("comment_form.html", comment=element)


@comment.route("/comments/<int:comment_id>/delete")
def delete_comment(comment_id):
    element = data_manager.get_specific_record(comment_id, "comment")
    if element.get("question_id"):
        question_id = element.get("question_id")
    else:
        answer_id = element.get("answer_id")
        answer = data_manager.get_specific_record(answer_id, "answer")
        question_id = answer.get("question_id")
    data_manager.delete_comment(comment_id)
    return redirect(url_for("show_question", question_id=question_id))


def add_comment_to_database(record):
    record["message"] = request.form["message"]
    record["edited_number"] = 0
    record["submission_time"] = util.get_new_timestamp()
    data_manager.add_comment(record)
