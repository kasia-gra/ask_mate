import csv
import os
dirpath = os.path.dirname(__file__)
ANSWER_FILE_PATH = os.path.join(dirpath, ".sample_data/answer.csv")
QUESTION_FILE_PATH = os.path.join(dirpath, "sample_data/question.csv")


def get_dict_list_from_csv_file(option="question"):
    dicts_list = []
    filepath = get_file_path(option)
    with open(filepath, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for dictionary in reader:
            dicts_list.append(dictionary)
    return dicts_list


def save_to_file(data, option="answers"):
    with open(get_file_path(option), "w", newline="") as file:
        data = csv.DictWriter(file, fieldnames=get_headers_from_file(option))
        for element in data:
            data.writerow(element)


def get_headers_from_file(option="answers"):
    if option == "questions":
        with open(QUESTION_FILE_PATH, newline="") as file:
            data = csv.reader(file)
            return next(data)
    else:
        with open(ANSWER_FILE_PATH, newline="") as file:
            data = csv.reader(file)
            return next(data)


def add_record_to_data(record, data):
    data.append(record)
    return data


def get_file_path(option="answers"):
    if option == "answers":
        return ANSWER_FILE_PATH
    return QUESTION_FILE_PATH
