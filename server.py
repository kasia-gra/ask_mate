from flask import Flask, render_template, request, redirect
import connection
import data_manager


app = Flask(__name__)


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
        new_record["image"] = request.form["image"]
        data_manager.add_record_to_file(new_record, "questions")
        return redirect("/")
    return render_template("question_form.html", old_record=new_record, is_new=True)


@app.route("/question/<question_id>")
def show_question(question_id):
    record = data_manager.get_old_record(question_id, "questions")
    return render_template("question_details.html", record=record)


@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    data_manager.delete_record_from_file(question_id, "questions")
    return redirect("/")


@app.route("/question/<question_id>/edit", methods=["POST", "GET"])
def edit_question(question_id):
    old_record = data_manager.get_old_record(question_id, "questions")
    if request.method == "POST":
        old_record["title"] = request.form["title"]
        old_record["message"] = request.form["description"]
        old_record["image"] = request.form["image"]
        data_manager.edit_record_in_file(old_record, "questions")
        return redirect("/question/<question_id>")
    return render_template("question_form.html", old_record=old_record, is_new=False)


if __name__ == "__main__":
    app.run(
        host='127.0.0.1',
        port=8000,
        debug=True,
    )
