from flask import request, redirect, make_response, Blueprint
import data_manager
vote = Blueprint('vote', __name__, template_folder='templates')


@vote.route("/question/<question_id>/<vote>")
def question_vote(question_id, vote):
    if request.cookies.get("q" + question_id) != "voted":
        res = make_response(redirect("/"))
        res.set_cookie("q" + question_id, "voted")
        data_manager.update_vote_number("question", str(question_id), vote)
        return res
    return redirect("/list")


@vote.route("/answer/<answer_id>/vote_up")
def answer_vote_up(answer_id):
    answer = data_manager.get_specific_record(answer_id, "answer")
    question_id = answer.get("question_id")
    if request.cookies.get("a" + str(answer_id)) != "voted":
        res = make_response(redirect("/question/" + str(question_id)))
        res.set_cookie("a" + str(answer_id), "voted")
        data_manager.update_vote_number("answer", str(answer_id), "up")
        return res
    return redirect("/question/" + str(question_id))


@vote.route("/answer/<answer_id>/vote_down")
def answer_vote_down(answer_id):
    answer = data_manager.get_specific_record(answer_id, "answer")
    question_id = answer.get("question_id")
    if request.cookies.get("a" + str(answer_id)) != "voted":
        res = make_response(redirect("/question/" + str(question_id)))
        res.set_cookie("a" + str(answer_id), "voted")
        data_manager.update_vote_number("answer", str(answer_id), "down")
        return res
    return redirect("/question/" + str(question_id))

