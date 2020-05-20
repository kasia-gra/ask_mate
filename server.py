from flask import Flask, render_template, request, redirect, make_response
import connection, data_manager, util



app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = data_manager.UPLOAD_FOLDER

@app.route("/")
@app.route("/list", methods=['GET', 'POST'])
def questions_list():
    all_questions = connection.format_dictionary_data()
    if request.method == 'POST':
        sort_by = request.form.get("sort_by")
    else:
        sort_by = "submission_time-asc"
    all_questions = connection.sort_dictionary(all_questions, sort_by)
    return render_template("question_list.html", all_questions=all_questions, sort_by=sort_by)


@app.route("/question", methods=["POST", "GET"])
def add_question():
    new_record = {}
    if request.method == "POST":
        new_record["title"] = request.form["title"]
        new_record["message"] = request.form["description"]
        file = request.files['file']
        new_record["image"] = util.save_image(file, app.config['UPLOAD_FOLDER'])
        data_manager.add_record_to_file(new_record, "questions")
        return redirect("/")
    return render_template("question_form.html", old_record=new_record, is_new=True)


@app.route("/question/<question_id>")
def show_question(question_id):
    record = data_manager.get_old_record(question_id, "questions")
    all_answers = data_manager.read_all_items_from_file_by_option("answers")
    answers_for_question_id = []
    data_manager.increase_view_number(question_id)
    for answer in all_answers:
        if answer.get("question_id") == question_id:
            answer["submission_time"] = util.change_timestamp_to_date(answer.get("submission_time"))
            answers_for_question_id.append(answer)
    return render_template("question_details.html", record=record, answers=answers_for_question_id, img_path=data_manager.UPLOAD_FOLDER)


@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    all_answers = data_manager.read_all_items_from_file_by_option("answers")
    for answer in all_answers:
        if answer.get("question_id") == question_id:
            data_manager.delete_answer_from_file(answer.get("id"))
    data_manager.delete_question_from_file(question_id)
    return redirect("/")


@app.route("/question/<question_id>/edit", methods=["POST", "GET"])
def edit_question(question_id):
    old_record = data_manager.get_old_record(question_id, "questions")
    if request.method == "POST":
        old_record["title"] = request.form["title"]
        old_record["message"] = request.form["description"]
        file = request.files['file']
        old_record["image"] = util.save_image(file, app.config['UPLOAD_FOLDER'])
        data_manager.edit_record_in_file(old_record, "questions")
        return redirect("/question/" + question_id)
    return render_template("question_form.html", old_record=old_record, is_new=False)


@app.route("/answer/<answer_id>/delete")
def delete_answer(answer_id):
    old_record = data_manager.get_old_record(answer_id, "answers")
    data_manager.delete_answer_from_file(answer_id)
    return redirect("/question/" + old_record["question_id"])


@app.route("/question/<question_id>/new-answer", methods=["POST", "GET"])
def add_answer(question_id):
    new_record = {"question_id": str(question_id)}
    if request.method == "POST":
        new_record["message"] = request.form["description"]
        new_record["image"] = request.form["image"]
        data_manager.add_record_to_file(new_record, "answers")
        return redirect("/question/" + question_id)
    return render_template("answer_form.html", old_record=new_record)


@app.route("/question/<question_id>/vote_up")
def question_vote_up(question_id):
    if request.cookies.get("q" + question_id) != "voted":
        res = make_response(redirect("/"))
        res.set_cookie("q" + question_id, "voted")
        data_manager.update_vote_number("questions", question_id, "up")
        return res
    return redirect("/")


@app.route("/question/<question_id>/vote_down")
def question_vote_down(question_id):
    if request.cookies.get("q" + question_id) != "voted":
        res = make_response(redirect("/"))
        res.set_cookie("q" + question_id, "voted")
        data_manager.update_vote_number("questions", question_id, "down")
        return res
    return redirect("/")


@app.route("/answer/<answer_id>/vote_up")
def answer_vote_up(answer_id):
    answer = data_manager.get_old_record(answer_id, "answers")
    question_id = answer.get("question_id")
    if request.cookies.get("a" + answer_id) != "voted":
        res = make_response(redirect("/question/" + question_id))
        res.set_cookie("a" + answer_id, "voted")
        data_manager.update_vote_number("answers", answer_id, "up")
        return res
    return redirect("/question/" + question_id)


@app.route("/answer/<answer_id>/vote_down")
def answer_vote_down(answer_id):
    answer = data_manager.get_old_record(answer_id, "answers")
    question_id = answer.get("question_id")
    if request.cookies.get("a" + answer_id) != "voted":
        res = make_response(redirect("/question/" + question_id))
        res.set_cookie("a" + answer_id, "voted")
        data_manager.update_vote_number("answers", answer_id, "down")
        return res
    return redirect("/question/" + question_id)


@app.route("/question/upload_image", methods=["POST", "GET"])
def upload_image():
    if request.method == 'POST':
        file = request.files['file']
        if file and util.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return str(filename)
            # return redirect("/question/upload_image")
    return render_template("upload_image.html")


if __name__ == "__main__":
    app.run(
        host='127.0.0.1',
        port=8000,
        debug=True,
    )
