from flask import Flask, render_template, request, redirect, make_response, url_for
import data_manager, util
import jinja2

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = data_manager.UPLOAD_FOLDER


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
    search_phrase = request.args.get('search_phrase')
    if search_phrase:
        return search_for_questions(search_phrase)
    return render_template("question_list.html", all_questions=all_questions, sort_by=sort_by, search_phrase=search_phrase)


# @app.route("/list", methods=['GET', 'POST'])
# def questions_list():
#     all_questions = data_manager.get_all_records("question")
#     if request.method == 'POST':
#         sort_by = request.form.get("sort_by")
#     else:
#         sort_by = "submission_time-DESC"
#     all_questions = util.sort_dictionary(all_questions, sort_by)
#     search_phrase = request.args.get('search_phrase')
#     if search_phrase:
#         return search_for_questions(search_phrase)
#     return render_template("question_list.html", all_questions=all_questions, sort_by=sort_by, search_phrase=search_phrase)


@app.route("/question", methods=["POST", "GET"])
def add_question():
    new_record = {}
    if request.method == "POST":
        new_record["title"] = request.form["title"]
        new_record["submission_time"] = util.get_new_timestamp()
        new_record["message"] = request.form["description"]
        if 'file' in request.files:
            file = request.files['file']
            new_record["image"] = util.save_image(file, app.config['UPLOAD_FOLDER'], "question")
        if not new_record["image"]:
            new_record["image"] = ""
        data_manager.add_record(new_record, "question")
        return redirect("/list")
    return render_template("question_form.html", old_record=new_record, is_new=True)


@app.route("/question/<question_id>")
def show_question(question_id):
    record = data_manager.get_specific_record(question_id, "question")
    tags = data_manager.get_tags_for_questions(question_id)
    all_answers_for_question = data_manager.get_answers_for_question(question_id)
    data_manager.increase_view_number(question_id)
    question_comments = data_manager.get_question_comments(question_id)
    return render_template("question_details.html", record=record, answers=all_answers_for_question, question_comments=question_comments, tags=tags)


@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    all_answers = data_manager.get_all_records("answer")
    for answer in all_answers:
        if answer.get("question_id") == question_id:
            data_manager.delete_record(answer.get("id"), "answer")
            data_manager.delete_connected_comment(answer.get("id"))
    data_manager.delete_connected_comment(question_id)
    data_manager.delete_record(question_id, "question")
    return redirect("/list")


@app.route("/question/<question_id>/edit", methods=["POST", "GET"])
def edit_question(question_id):
    old_record = data_manager.get_specific_record(question_id, "question")
    if request.method == "POST":
        old_record["title"] = request.form["title"]
        old_record["submission_time"] = util.get_new_timestamp()
        old_record["message"] = request.form["description"]
        if 'file' in request.files:
            file = request.files['file']
            old_record["image"] = util.save_image(file, app.config['UPLOAD_FOLDER'], "question")
        if not old_record["image"]:
            old_record["image"] = ""
        data_manager.edit_record(old_record, "question")
        return redirect("/question/" + str(question_id))
    return render_template("question_form.html", old_record=old_record, is_new=False)


@app.route("/answer/<answer_id>/delete")
def delete_answer(answer_id):
    old_record = data_manager.get_specific_record(answer_id, "answer")
    data_manager.delete_record(answer_id, "answer")
    return redirect("/question/" + str(old_record["question_id"]))


@app.route("/question/<question_id>/new-answer", methods=["POST", "GET"])
def add_answer(question_id):
    new_record = {"question_id": str(question_id)}
    if request.method == "POST":
        new_record["message"] = request.form["description"]
        new_record["submission_time"] = util.get_new_timestamp()
        if 'file' in request.files:
            file = request.files['file']
            new_record["image"] = util.save_image(file, app.config['UPLOAD_FOLDER'], "answer", str(question_id))
        if not new_record["image"]:
            new_record["image"] = ""
        data_manager.add_record(new_record, "answer")
        return redirect("/question/" + str(question_id))
    return render_template("answer_form.html", old_record=new_record, is_new=True)


@app.route("/answer/<answer_id>/edit", methods=["POST", "GET"])
def edit_answer(answer_id):
    old_record = data_manager.get_specific_record(answer_id, "answer")
    if request.method == "POST":
        old_record["submission_time"] = util.get_new_timestamp()
        old_record["message"] = request.form["description"]
        if 'file' in request.files:
            file = request.files['file']
            old_record["image"] = util.save_image(file, app.config['UPLOAD_FOLDER'], "answer", str(old_record["question_id"]))
        if not old_record["image"]:
            old_record["image"] = ""
        data_manager.edit_record(old_record, "answer")
        return redirect("/question/" + str(old_record["question_id"]))
    return render_template("answer_form.html", old_record=old_record, is_new=False)


@app.route("/question/<question_id>/<vote>")
def question_vote(question_id, vote):
    if request.cookies.get("q" + question_id) != "voted":
        res = make_response(redirect("/"))
        res.set_cookie("q" + question_id, "voted")
        data_manager.update_vote_number("question", str(question_id), vote)
        return res
    return redirect("/list")


@app.route("/answer/<answer_id>/vote_up")
def answer_vote_up(answer_id):
    answer = data_manager.get_specific_record(answer_id, "answer")
    question_id = answer.get("question_id")
    if request.cookies.get("a" + str(answer_id)) != "voted":
        res = make_response(redirect("/question/" + str(question_id)))
        res.set_cookie("a" + str(answer_id), "voted")
        data_manager.update_vote_number("answer", str(answer_id), "up")
        return res
    return redirect("/question/" + str(question_id))


@app.route("/answer/<answer_id>/vote_down")
def answer_vote_down(answer_id):
    answer = data_manager.get_specific_record(answer_id, "answer")
    question_id = answer.get("question_id")
    if request.cookies.get("a" + str(answer_id)) != "voted":
        res = make_response(redirect("/question/" + str(question_id)))
        res.set_cookie("a" + str(answer_id), "voted")
        data_manager.update_vote_number("answer", str(answer_id), "down")
        return res
    return redirect("/question/" + str(question_id))


@app.route("/question/<int:question_id>/new-comment", methods=["POST", "GET"])
def comment_question(question_id):
    new_record = {"question_id": question_id}
    if request.method == "POST":
        new_record["message"] = request.form["message"]
        new_record["edited_number"] = 0
        new_record["submission_time"] = util.get_new_timestamp()
        new_record["answer_id"] = None
        data_manager.add_comment(new_record)
        return redirect(url_for("show_question", question_id=str(question_id)))
    return render_template("comment_form.html", question_id=str(question_id))


@app.route('/search_phrase')
def search_for_questions(search_phrase):
    search_results_questions = data_manager.search_for_phrase_questions(search_phrase)
    search_results_answers = data_manager.search_for_phrase_answers(search_phrase)
    return render_template("search_results.html", all_questions=search_results_questions, answers=search_results_answers, search_phrase=search_phrase)


@app.route('/question/<question_id>/tag/<tag_id>/delete')
def delete_tag(question_id, tag_id):
    pass


if __name__ == "__main__":
    app.run(
        host='127.0.0.1',
        port=8000,
        debug=True,
    )
