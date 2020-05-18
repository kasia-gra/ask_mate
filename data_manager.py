import csv

ANSWER_FILE_PATH = "sample_data/answer.csv"
QUESTION_FILE_PATH = "sample_data/question.csv"
QUESTION_HEADERS = ["Id", "Submission time", "View number", "Vote number", "Title", "Message", "Image path"]
ANSWER_HEADERS = ["Id", "Submission time", "Vote number", "Question id", "Message", "Image path"]


def save_questions_to_file(dictionary):
    with open(QUESTION_FILE_PATH, "w", newline="") as file:
        csv.DictWriter(file, fieldnames=QUESTION_HEADERS)

