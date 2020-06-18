from flask import redirect, Blueprint, session, abort, render_template
import data_manager

vote = Blueprint('vote', __name__, template_folder='templates')


@vote.route("/question/<question_id>/<vote>")
def question_vote(question_id, vote):
    if 'username' not in session:
        abort(401)
    username = session['username']
    user_id = data_manager.get_user_id(username).get("id")
    user_votes = data_manager.get_user_votes(user_id)
    question = data_manager.get_specific_record(question_id, "question")
    if int(user_id) == int(question.get("user_id")):
        return render_your_question_page("question")
    for voter in user_votes:
        print(voter["question_id"])
        print(question_id)
        if voter["question_id"] and int(voter["question_id"]) == int(question_id) and int(user_id) == int(voter["user_id"]):
            return render_already_voted_page("question")
    if vote == "down":
        data_manager.update_vote_number("question", str(question_id), "down")
        data_manager.update_reputation(question["user_id"], -2)
    else:
        data_manager.update_vote_number("question", str(question_id), "up")
        data_manager.update_reputation(question["user_id"], 5)
    data_manager.update_question_vote(user_id, question_id)
    return redirect("/question/" + question_id)


@vote.route("/answer/<answer_id>/<voting_type>")
def answer_vote(answer_id, voting_type):
    if 'username' not in session:
        abort(401)
    username = session['username']
    user_id = data_manager.get_user_id(username).get("id")
    user_votes = data_manager.get_user_votes(user_id)
    answer = data_manager.get_specific_record(answer_id, "answer")
    if int(user_id) == int(answer.get("user_id")):
        return render_your_question_page("answer")
    for vote in user_votes:
        if vote["answer_id"] and int(vote["answer_id"]) == int(answer_id) and int(user_id) == int(vote["user_id"]):
            return render_already_voted_page("answer")
    if voting_type == "down":
        data_manager.update_vote_number("answer", str(answer_id), "down")
        data_manager.update_reputation(answer["user_id"], -2)
    else:
        data_manager.update_vote_number("answer", str(answer_id), "up")
        data_manager.update_reputation(answer["user_id"], 10)
    data_manager.update_answer_vote(user_id, answer_id)
    return redirect("/question/" + str(answer.get("question_id")))


def render_already_voted_page(option):
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


def render_your_question_page(option):
    username = session['username']
    user_id = session['user_id']
    return render_template(
        "error_page.html",
        error_code="",
        error_message="This is your {}".format(option),
        message="",
        user_id=user_id,
        username=username
    )
