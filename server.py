from flask import Flask, render_template, request, redirect, url_for
import connection
import data_manager


app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"

@app.route("/list", methods=['GET', 'POST'])
def questions_list():
    all_questions = connection.format_dictionary_data()
    if request.method == 'POST':
        sort_by = request.form.get("sort_by")
    else: sort_by = "submission_time-asc"
    all_questions = connection.sort_dictionary(all_questions, sort_by)
    return render_template("question_list.html", all_questions=all_questions, sort_by=sort_by)


@app.route("/question", methods=["POST", "GET"])
def add_question():
    all_questions = data_manager.get_dict_list_from_csv_file()
    new_record = {}
    if request.method == "POST":
        new_record["id"] = str(int(len(all_questions)) + 1)
        new_record["submission_time"] = 0
        new_record["view_number"] = 0
        new_record["vote_number"] = 0
        new_record["title"] = request.form["title"]
        new_record["message"] = request.form["description"]
        new_record["image"] = request.form["image"]
        data_manager.add_record_to_data(new_record, all_questions)
        data_manager.save_to_file(all_questions, "questions")
        return redirect("/")
    return render_template("question_form.html")


@app.route("/question/<question_id>")
def show_question(question_id):
    return render_template("question_details.html")


@app.route("/question/<question_id>/edit", methods=["POST", "GET"])
def edit_question(question_id):
    # seek CSV file for entry with this ID and show this results in question_details
    question_details = {
        "Id": 1,
        "Submission time": 0,
        "View number": 0,
        "Vote number": 0,
        "Title": "Question title",
        "Message": "Question Message",
        "Image Path": "Image Path"
    }
    if request.method == "POST":
        question_title = request.form["title"]
        question_message = request.form["description"]
        image_path = request.form["image"]
        # save modified elements into CSV file and redirect
        return redirect("/question/<question_id>")
    return render_template("question_form.html", question_details=question_details)


if __name__ == "__main__":
    app.run(
        host='127.0.0.1',
        port=8000,
        debug=True,
    )
