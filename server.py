from flask import Flask, render_template, request, session
import data_manager

from question_handler import question
from answer_handler import answer
from comment_handler import comment
from vote_handler import vote
from tag_handler import tag
from registration_handler import registration
from user_handler import user

app = Flask(__name__)
app.register_blueprint(question)
app.register_blueprint(answer)
app.register_blueprint(comment)
app.register_blueprint(vote)
app.register_blueprint(tag)
app.register_blueprint(registration)
app.register_blueprint(user)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/")
def homepage():
    if 'username' in session:
        logged_status = True
        username = session['username']
        user_id = session['user_id']
    else:
        logged_status = False
        user_id = None
        username = None
    five_questions = data_manager.get_five_records("question")
    if request.method == 'POST':
        sort_by = request.form.get("sort_by")
        five_questions = data_manager.get_sorted_questions(sort_by)
    else:
        sort_by = "submission_time-DESC"
    five_questions = prepare_questions_to_display(five_questions)
    search_phrase = request.args.get('search_phrase')
    if search_phrase:
        return search_for_questions(search_phrase)
    return render_template(
        "question_list.html",
        all_questions=five_questions,
        sort_by=sort_by,
        search_phrase=search_phrase,
        is_homepage=True,
        logged=logged_status,
        user_id=user_id,
        username=username
    )


@app.route("/list", methods=['GET', 'POST'])
def questions_list():
    if 'username' in session:
        logged_status = True
        username = session['username']
        user_id = session['user_id']
    else:
        logged_status = False
        user_id = None
        username = None
    sort_by = request.args.get('sort_by')
    if sort_by:
        criteria_and_direction = sort_by.split("-")
        all_questions = data_manager.get_sorted_questions(criteria_and_direction)
    else:
        all_questions = data_manager.get_all_records("question")
    all_questions = prepare_questions_to_display(all_questions)
    search_phrase = request.args.get('search_phrase')
    if search_phrase:
        return search_for_questions(search_phrase)
    return render_template(
        "question_list.html",
        all_questions=all_questions,
        sort_by=sort_by,
        search_phrase=search_phrase,
        is_homepage=False,
        logged=logged_status,
        user_id=user_id,
        username=username
    )


def prepare_questions_to_display(all_questions):
    message_max_length = 800
    title_max_length = 53
    for record in all_questions:
        record["number_of_answers"] = data_manager.count_answers_for_question(record["id"])["count"]
        if len(record["title"]) >= title_max_length:
            record["title"] = record["title"][:title_max_length] + "..."
        if len(record["message"]) >= message_max_length:
            record["message"] = record["message"][:message_max_length] + "..."
    return all_questions


@app.route("/question/<question_id>")
def show_question(question_id):
    if 'username' in session:
        logged_status = True
        username = session['username']
        user_id = session['user_id']
    else:
        logged_status = False
        user_id = None
        username = None
    record = data_manager.get_specific_record(question_id, "question")
    tags = data_manager.get_tags_for_questions(question_id)
    all_answers_for_question = data_manager.get_answers_for_question(question_id)
    question_comments, answers_comments, answers_id_list, comment_id_list = [], [], [], []
    for element in all_answers_for_question:
        answers_id_list.append(element.get("id"))
    data_manager.increase_view_number(question_id)
    record["number_of_answers"] = data_manager.count_answers_for_question(record["id"])["count"]
    question_comments = data_manager.get_question_comments(question_id)
    if answers_id_list:
        answers_comments = data_manager.get_answers_comments(answers_id_list)
        for element in answers_comments:
            comment_id_list.append(element.get("answer_id"))
    return render_template(
        "question_details.html",
        record=record,
        answers=all_answers_for_question,
        question_comments=question_comments,
        tags=tags,
        answers_comments=answers_comments,
        comment_id_list=comment_id_list,
        logged=logged_status,
        user_id=user_id,
        username=username
    )


@app.route('/search_phrase')
def search_for_questions(search_phrase):
    if 'username' in session:
        logged_status = True
        username = session['username']
        user_id = session['user_id']
    else:
        logged_status = False
        user_id = None
        username = None
    search_results_questions = data_manager.search_for_phrase_questions(search_phrase)
    search_results_questions = prepare_questions_to_display(search_results_questions)
    search_results_answers = data_manager.search_for_phrase_answers(search_phrase)
    return render_template(
        "search_results.html",
        all_questions=search_results_questions,
        answers=search_results_answers,
        search_phrase=search_phrase,
        logged=logged_status,
        user_id=user_id,
        username=username
    )


@app.errorhandler(400)
def page_not_found(error):
    return render_template(
        "error_page.html",
        error_code="400",
        error_message="Bad Request",
        message="Sorry, I can't found that request in my database."
    ), 400


@app.errorhandler(401)
def page_not_found(error):
    return render_template(
        "error_page.html",
        error_code="401",
        error_message="Unauthorized",
        message="You need to sign in to do that!"
    ), 401


@app.errorhandler(403)
def page_not_found(error):
    return render_template(
        "error_page.html",
        error_code="403",
        error_message="Forbidden",
        message="You don't have access to do that!"
    ), 403


@app.errorhandler(404)
def page_not_found(error):
    return render_template(
        "error_page.html",
        error_code="403",
        error_message="Not Found",
        message="Sorry, Page doesn't exist!"
    ), 404


if __name__ == "__main__":
    app.run(
        host='127.0.0.1',
        port=8000,
        debug=True,
    )
