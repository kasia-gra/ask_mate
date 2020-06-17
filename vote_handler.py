from flask import request, redirect, make_response, Blueprint, session, abort, render_template
import data_manager

vote = Blueprint('vote', __name__, template_folder='templates')


'''
    REWORK ALL VOTE HANDLER
    FUNCTION IS NOT ABSTRACT ENOUGH
'''


@vote.route("/question/<question_id>/<vote>")
def question_vote(question_id, vote):
    try_to_raise_401_error()
    question = data_manager.get_specific_record(question_id, "question")
    if int(session['user_id']) == int(question["user_id"]):
        abort(403)
    if request.cookies.get("q" + question_id) != "voted":
        res = make_response(redirect("/"))
        res.set_cookie("q" + question_id, "voted")
        data_manager.update_vote_number("question", str(question_id), vote)
        if vote == "up":
            data_manager.update_reputation(question["user_id"], 5)
        else:
            data_manager.update_reputation(question["user_id"], -2)
        return res
    return render_error_page("question")


@vote.route("/answer/<answer_id>/vote_up")
def answer_vote_up(answer_id):
    try_to_raise_401_error()
    answer = data_manager.get_specific_record(answer_id, "answer")
    question_id = answer.get("question_id")
    if int(session['user_id']) == int(answer["user_id"]):
        abort(403)
    if request.cookies.get("a" + str(answer_id)) != "voted":
        res = make_response(redirect("/question/" + str(question_id)))
        res.set_cookie("a" + str(answer_id), "voted")
        data_manager.update_vote_number("answer", str(answer_id), "up")
        data_manager.update_reputation(answer["user_id"], 10)
        return res
    return render_error_page("answer")


@vote.route("/answer/<answer_id>/vote_down")
def answer_vote_down(answer_id):
    try_to_raise_401_error()
    answer = data_manager.get_specific_record(answer_id, "answer")
    question_id = answer.get("question_id")
    if int(session['user_id']) == int(answer["user_id"]):
        abort(403)
    if request.cookies.get("a" + str(answer_id)) != "voted":
        res = make_response(redirect("/question/" + str(question_id)))
        res.set_cookie("a" + str(answer_id), "voted")
        data_manager.update_vote_number("answer", str(answer_id), "down")
        data_manager.update_reputation(answer["user_id"], -2)
        return res
    return render_error_page("answer")


def render_error_page(option):
    username = session['username']
    user_id = session['user_id']
    return render_template(
        "error_page.html",
        error_code="",
        error_message="Already voted",
        message="You already voted on {}!".format(option),
        user_id=user_id,
        username=username
    )


def try_to_raise_401_error():
    if 'username' not in session:
        abort(401)
