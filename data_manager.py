import csv
from datetime import datetime

ANSWER_FILE_PATH = "sample_data/answer.csv"
QUESTION_FILE_PATH = "sample_data/question.csv"
QUESTION_HEADERS = ["Id", "Submission time", "View number", "Vote number", "Title", "Message", "Image path"]
ANSWER_HEADERS = ["Id", "Submission time", "Vote number", "Question id", "Message", "Image path"]


def get_dict_list_from_csv_file():
    dicts_list = []
    with open(QUESTION_FILE_PATH, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for dictionary in reader:
            dicts_list.append(dictionary)
    return dicts_list


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

