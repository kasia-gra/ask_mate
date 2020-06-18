from flask import Flask, render_template, request, session
import data_manager
import util

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
    username, logged_user_id = util.set_user_details_based_on_logged_status()
    five_questions = data_manager.get_five_records("question")
    if request.method == 'POST':
        sort_by = request.form.get("sort_by")
        five_questions = data_manager.get_sorted_questions(sort_by)
    else:
        sort_by = "submission_time-DESC"
    five_questions = util.prepare_questions_to_display(five_questions)
    search_phrase = request.args.get('search_phrase')
    if search_phrase:
        return search_for_questions(search_phrase)
    return render_template(
        "question_list.html",
        all_questions=five_questions,
        sort_by=sort_by,
        search_phrase=search_phrase,
        is_homepage=True,
        user_id=logged_user_id,
        username=username
    )


@app.route("/list", methods=['GET', 'POST'])
def questions_list():
    username, logged_user_id = util.set_user_details_based_on_logged_status()
    sort_by = request.args.get('sort_by')
    if sort_by:
        criteria_and_direction = sort_by.split("-")
        all_questions = data_manager.get_sorted_questions(criteria_and_direction)
    else:
        all_questions = data_manager.get_all_records("question")
    all_questions = util.prepare_questions_to_display(all_questions)
    search_phrase = request.args.get('search_phrase')
    if search_phrase:
        return search_for_questions(search_phrase)
    return render_template(
        "question_list.html",
        all_questions=all_questions,
        sort_by=sort_by,
        search_phrase=search_phrase,
        is_homepage=False,
        user_id=logged_user_id,
        username=username
    )


@app.route("/question/<question_id>")
def show_question(question_id):
    username, logged_user_id = util.set_user_details_based_on_logged_status()
    selected_question = data_manager.get_specific_record(question_id, "question")
    tags = data_manager.get_tags_for_questions(question_id)
    all_answers_for_question = data_manager.get_answers_for_question(question_id)
    question_comments, answers_comments, answers_id_list, comment_id_list = [], [], [], []
    for element in all_answers_for_question:
        answers_id_list.append(element.get("id"))
    data_manager.increase_view_number(question_id)
    selected_question["number_of_answers"] = data_manager.count_answers_for_question(selected_question["id"])["count"]
    question_comments = data_manager.get_question_comments(question_id)
    if answers_id_list:
        answers_comments = data_manager.get_answers_comments(answers_id_list)
        for element in answers_comments:
            comment_id_list.append(element.get("answer_id"))
    return render_template(
        "question_details.html",
        record=selected_question,
        answers=all_answers_for_question,
        question_comments=question_comments,
        tags=tags,
        answers_comments=answers_comments,
        comment_id_list=comment_id_list,
        user_id=logged_user_id,
        username=username
    )


@app.route('/search_phrase')
def search_for_questions(search_phrase):
    username, logged_user_id = util.set_user_details_based_on_logged_status()
    search_results_questions = data_manager.search_for_phrase_questions(search_phrase)
    search_results_questions = util.prepare_questions_to_display(search_results_questions)
    search_results_answers = data_manager.search_for_phrase_answers(search_phrase)
    return render_template(
        "search_results.html",
        all_questions=search_results_questions,
        answers=search_results_answers,
        search_phrase=search_phrase,
        user_id=logged_user_id,
        username=username
    )


@app.errorhandler(400)
def page_not_found(error):
    error_code = "400"
    error_message = "Bad Request"
    message = "Sorry, I can't found that request in my database."
    return render_error_page(error_code, error_message, message)


@app.errorhandler(401)
def page_not_found(error):
    error_code = "401"
    error_message = "Unauthorized"
    message = "You need to sign in to do that!"
    return render_error_page(error_code, error_message, message)


@app.errorhandler(403)
def page_not_found(error):
    error_code = "403"
    error_message = "Forbidden"
    message = "You don't have access to do that!"
    return render_error_page(error_code, error_message, message)


@app.errorhandler(404)
def page_not_found(error):
    error_code = "404"
    error_message = "Not Found"
    message = "Sorry, Page doesn't exist!"
    return render_error_page(error_code, error_message, message)


def render_error_page(error_code, error_message, message):
    username, logged_user_id = util.set_user_details_based_on_logged_status()
    return render_template(
        "error_page.html",
        error_code=error_code,
        error_message=error_message,
        message=message,
        user_id=logged_user_id,
        username=username
    ), error_code


if __name__ == "__main__":
    app.run(
        host='127.0.0.1',
        port=8000,
        debug=True,
    )
