import csv

ANSWER_FILE_PATH = "sample_data/answer.csv"
QUESTION_FILE_PATH = "sample_data/question.csv"
QUESTION_HEADERS = ["Id", "Submission time", "View number", "Vote number", "Title", "Message", "Image path"]
ANSWER_HEADERS = ["Id", "Submission time", "Vote number", "Question id", "Message", "Image path"]


def save_questions_to_file(data_in_dict_format):
    with open(QUESTION_FILE_PATH, "w", newline="") as file:
        data = csv.DictWriter(file, fieldnames=QUESTION_HEADERS)
        for element in data_in_dict_format:
            data.writerow(element)


def save_answers_to_file(data_in_dict_format):
    with open(ANSWER_FILE_PATH, "w", newline="") as file:
        data = csv.DictWriter(file, fieldnames=ANSWER_HEADERS)
        for element in data_in_dict_format:
            data.writerow(element)

