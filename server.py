from flask import Flask, render_template, request, redirect
import data_manager

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/question", methods=["POST", "GET"])
def add_question():
    if request.method == "POST":
        question_title = request.form["title"]
        question_message = request.form["description"]
        image_path = request.form["image"]
        # save new element into CSV file and redirect
        return redirect("/")
    return render_template("question.html")


@app.route("/question/<question_id>/edit", methods=["POST", "GET"])
def edit_question(question_id):
    # seek CSV file for entry with this ID and show this results in question_details
    question_details = {
        id: 1,
        "Submission Time": 0,
        "View number": 0,
        "Vote number": 0,
        "Question title": "Question title",
        "Question message": "Question Message",
        "Image Path": "Image Path"
    }
    if request.method == "POST":
        question_title = request.form["title"]
        question_message = request.form["description"]
        image_path = request.form["image"]
        # save modified elements into CSV file and redirect
        return redirect("/")
    return render_template("question.html", question_details=question_details)


if __name__ == "__main__":
    app.run(
        host='127.0.0.1',
        port=8000,
        debug=True,
    )
