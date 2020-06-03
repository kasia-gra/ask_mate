from flask import Flask, render_template, request, redirect, make_response, url_for
import data_manager
from question_handler import question
from answer_handler import answer
from comment_handler import comment
from vote_handler import vote
from tag_handler import tag


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = data_manager.UPLOAD_FOLDER
app.register_blueprint(question)
app.register_blueprint(answer)
app.register_blueprint(comment)
app.register_blueprint(vote)
app.register_blueprint(tag)


@app.route("/")
def homepage():
    five_questions = data_manager.get_five_records("question")
    if request.method == 'POST':
        sort_by = request.form.get("sort_by")
        five_questions = data_manager.get_sorted_questions(sort_by)
    else:
        sort_by = "submission_time-DESC"
    search_phrase = request.args.get('search_phrase')
    if search_phrase:
        return search_for_questions(search_phrase)
    return render_template("index.html", all_questions=five_questions, sort_by=sort_by, search_phrase=search_phrase)


@app.route("/list", methods=['GET', 'POST'])
def questions_list():
    sort_by = request.args.get('sort_by')
    if sort_by:
        criteria_and_direction = sort_by.split("-")
        all_questions = data_manager.get_sorted_questions(criteria_and_direction)
    else:
        all_questions = data_manager.get_all_records("question")
    for question in all_questions:
        question["number_of_answers"] = len(data_manager.get_answers_for_question(question.get("id")))
    search_phrase = request.args.get('search_phrase')
    if search_phrase:
        return search_for_questions(search_phrase)
    return render_template("question_list.html", all_questions=all_questions, sort_by=sort_by, search_phrase=search_phrase)


@app.route("/question/<question_id>")
def show_question(question_id):
    record = data_manager.get_specific_record(question_id, "question")
    tags = data_manager.get_tags_for_questions(question_id)
    all_answers_for_question = data_manager.get_answers_for_question(question_id)
    question_comments, answers_comments, answers_id_list, comment_id_list = [], [], [], []
    for answer in all_answers_for_question:
        answers_id_list.append(answer.get("id"))
    data_manager.increase_view_number(question_id)
    question_comments = data_manager.get_question_comments(question_id)
    if answers_id_list:
        answers_comments = data_manager.get_answers_comments(answers_id_list)
        for comment in answers_comments:
            comment_id_list.append(comment.get("answer_id"))
    return render_template(
                    "question_details.html",
                    record=record,
                    answers=all_answers_for_question,
                    question_comments=question_comments,
                    tags=tags,
                    answers_comments=answers_comments,
                    comment_id_list=comment_id_list
                    )


@app.route('/search_phrase')
def search_for_questions(search_phrase):
    search_results_questions = data_manager.search_for_phrase_questions(search_phrase)
    search_results_answers = data_manager.search_for_phrase_answers(search_phrase)
    return render_template("search_results.html", all_questions=search_results_questions, answers=search_results_answers, search_phrase=search_phrase)


if __name__ == "__main__":
    app.run(
        host='127.0.0.1',
        port=8000,
        debug=True,
    )
