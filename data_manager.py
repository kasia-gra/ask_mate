import csv
import os
dirpath = os.path.dirname(__file__)
ANSWER_FILE_PATH = os.path.join(dirpath, ".sample_data/answer.csv")
QUESTION_FILE_PATH = os.path.join(dirpath, "sample_data/question.csv")
QUESTION_HEADERS = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
ANSWER_HEADERS = ["id", "submission_time", "vote_number", "question_id", "message", "image"]


def get_dict_list_from_csv_file(option):
    dicts_list = []
    filepath = get_file_path(option)
    with open(filepath, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for dictionary in reader:
            dicts_list.append(dictionary)
    return dicts_list


def save_to_file(all_records, option):
    if option == "questions":
        headers = QUESTION_HEADERS
    else:
        headers = ANSWER_HEADERS
    with open(get_file_path(option), "w", newline="") as file:
        data = csv.DictWriter(file, fieldnames=headers)
        for element in all_records:
            data.writerow(element)


def add_record_to_file(new_record, option):
    all_records = read_all_items_from_file_by_option(option)
    new_record["id"] = str(int(len(all_records)) + 1)
    new_record["submission_time"] = 0
    new_record["view_number"] = 0
    new_record["vote_number"] = 0
    all_records.append(new_record)
    save_to_file(all_records, option)


def edit_record_in_file(record, option):
    all_records = read_all_items_from_file_by_option(option)
    for element in all_records:
        if element["id"] == record["id"]:
            element["title"] = record["title"]
            element["message"] = record["description"]
            element["image"] = record["image"]
            element["submission_time"] = 0
    save_to_file(all_records, option)


def delete_record_from_file(record_id, option):
    all_records = read_all_items_from_file_by_option(option)
    all_records.pop(record_id)
    refreshed_id = 1
    for element in all_records:
        if element != "id":
            element["id"] = refreshed_id
            refreshed_id += 1
    save_to_file(all_records, option)


def read_all_items_from_file_by_option(option="questions"):
    if option == "questions":
        return get_dict_list_from_csv_file("questions")
    return get_dict_list_from_csv_file("answers")


def get_old_record(record_id, option):
    all_records = read_all_items_from_file_by_option(option)
    for element in all_records:
        if record_id == element["id"]:
            return element


def get_file_path(option="answers"):
    if option == "answers":
        return ANSWER_FILE_PATH
    return QUESTION_FILE_PATH
