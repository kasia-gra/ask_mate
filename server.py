from flask import Flask, render_template, request, redirect, make_response, url_for
import data_manager, util

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = data_manager.UPLOAD_FOLDER


@app.route("/")
@app.route("/list", methods=['GET', 'POST'])
def questions_list():
    all_questions = data_manager.get_all_records("question")
    if request.method == 'POST':
        sort_by = request.form.get("sort_by")
    else:
        sort_by = "submission_time-asc"
    all_questions = util.sort_dictionary(all_questions, sort_by)
    return render_template("question_list.html", all_questions=all_questions, sort_by=sort_by)


@app.route("/question", methods=["POST", "GET"])
def add_question():
    new_record = {}
    if request.method == "POST":
        new_record["title"] = request.form["title"]
        new_record["message"] = request.form["description"]
        if 'file' in request.files:
            file = request.files['file']
            new_record["image"] = util.save_image(file, app.config['UPLOAD_FOLDER'], "question")
        data_manager.add_record(new_record, "question")
        return redirect("/")
    return render_template("question_form.html", old_record=new_record, is_new=True)


@app.route("/question/<question_id>")
def show_question(question_id):
    record = data_manager.get_specific_record(question_id, "question")
    all_answers = data_manager.get_all_records("answer")
    data_manager.increase_view_number(question_id)
    for answer in all_answers:
        if str(answer.get("question_id")) == str(question_id):
            # answer["submission_time"] = util.change_timestamp_to_date(answer.get("submission_time"))
            pass
    question_comments = data_manager.get_question_comments(question_id)
    return render_template("question_details.html", record=record, answers=all_answers, question_comments=question_comments)


@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    all_answers = data_manager.get_all_records("answer")
    for answer in all_answers:
        if answer.get("question_id") == question_id:
            data_manager.delete_record(answer.get("id"), "answer")
    data_manager.delete_record(question_id, "question")
    return redirect("/")


@app.route("/question/<question_id>/edit", methods=["POST", "GET"])
def edit_question(question_id):
    old_record = data_manager.get_specific_record(question_id, "question")
    if request.method == "POST":
        old_record["title"] = request.form["title"]
        old_record["message"] = request.form["description"]
        if 'file' in request.files:
            file = request.files['file']
            old_record["image"] = util.save_image(file, app.config['UPLOAD_FOLDER'], "question")
        data_manager.edit_record(old_record, "question")
        return redirect("/question/" + question_id)
    return render_template("question_form.html", old_record=old_record, is_new=False)


@app.route("/answer/<answer_id>/delete")
def delete_answer(answer_id):
    old_record = data_manager.get_specific_record(answer_id, "answer")
    data_manager.delete_record(answer_id, "answer")
    return redirect("/question/" + old_record["question_id"])


@app.route("/question/<question_id>/new-answer", methods=["POST", "GET"])
def add_answer(question_id):
    new_record = {"question_id": str(question_id)}
    if request.method == "POST":
        new_record["message"] = request.form["description"]
        if 'file' in request.files:
            file = request.files['file']
            new_record["image"] = util.save_image(file, app.config['UPLOAD_FOLDER'], "answer", question_id)
        else:
            new_record["image"] = ""
        data_manager.add_record(new_record, "answer")
        return redirect("/question/" + question_id)
    return render_template("answer_form.html", old_record=new_record)


@app.route("/question/<question_id>/vote_up")
def question_vote_up(question_id):
    if request.cookies.get("q" + question_id) != "voted":
        res = make_response(redirect("/"))
        res.set_cookie("q" + question_id, "voted")
        data_manager.update_vote_number("question", question_id, "up")
        return res
    return redirect("/")


@app.route("/question/<question_id>/vote_down")
def question_vote_down(question_id):
    if request.cookies.get("q" + question_id) != "voted":
        res = make_response(redirect("/"))
        res.set_cookie("q" + question_id, "voted")
        data_manager.update_vote_number("question", question_id, "down")
        return res
    return redirect("/")


@app.route("/answer/<answer_id>/vote_up")
def answer_vote_up(answer_id):
    answer = data_manager.get_specific_record(answer_id, "answer")
    question_id = answer.get("question_id")
    if request.cookies.get("a" + answer_id) != "voted":
        res = make_response(redirect("/question/" + question_id))
        res.set_cookie("a" + answer_id, "voted")
        data_manager.update_vote_number("answer", answer_id, "up")
        return res
    return redirect("/question/" + question_id)


@app.route("/answer/<answer_id>/vote_down")
def answer_vote_down(answer_id):
    answer = data_manager.get_specific_record(answer_id, "answer")
    question_id = answer.get("question_id")
    if request.cookies.get("a" + answer_id) != "voted":
        res = make_response(redirect("/question/" + question_id))
        res.set_cookie("a" + answer_id, "voted")
        data_manager.update_vote_number("answer", answer_id, "down")
        return res
    return redirect("/question/" + question_id)


@app.route("/question/<int:question_id>/new-comment", methods=["POST", "GET"])
def comment_question(question_id):
    new_record = {"question_id": question_id}
    if request.method == "POST":
        new_record["message"] = request.form["message"]
        new_record["edited_count"] = 0
        new_record["submission_time"] = util.get_new_timestamp()
        new_record["answer_id"] = None
        data_manager.add_comment(new_record)
        return redirect(url_for("show_question", question_id=question_id))
    return render_template("comment_form.html", question_id=question_id)


if __name__ == "__main__":
    app.run(
        host='127.0.0.1',
        port=8000,
        debug=True,
    )
