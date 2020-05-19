import csv
import os
import util
dirpath = os.path.dirname(__file__)
ANSWER_FILE_PATH = os.path.join(dirpath, "sample_data/answer.csv")
QUESTION_FILE_PATH = os.path.join(dirpath, "sample_data/question.csv")
QUESTION_HEADERS = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
ANSWER_HEADERS = ["id", "submission_time", "vote_number", "question_id", "message", "image"]


def get_dict_list_from_csv_file(option):
    dicts_list = []
    filepath = get_file_path(option)
    with open(filepath, "r") as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=get_headers_by_option(option))
        for dictionary in reader:
            dicts_list.append(dictionary)
    return dicts_list


def save_to_file(all_records, option):
    with open(get_file_path(option), "w", newline="") as file:
        data = csv.DictWriter(file, fieldnames=get_headers_by_option(option))
        for element in all_records:
            data.writerow(element)


def add_record_to_file(new_record, option):
    all_records = read_all_items_from_file_by_option(option)
    if option == "questions":
        add_question(new_record, all_records)
    else:
        add_answer(new_record, all_records)
    all_records.append(new_record)
    save_to_file(all_records, option)


def add_question(new_record, all_records):
    new_record["id"] = str(len(all_records))
    new_record["submission_time"] = util.get_new_timestamp()
    new_record["view_number"] = 0
    new_record["vote_number"] = 0


def add_answer(new_record, all_records):
    new_record["id"] = str(len(all_records))
    new_record["submission_time"] = util.get_new_timestamp()
    new_record["vote_number"] = 0


def edit_record_in_file(record, option):
    all_records = read_all_items_from_file_by_option(option)
    if option == "questions":
        edit_question(record, all_records)
    else:
        edit_answer(record, all_records)
    save_to_file(all_records, option)


def edit_question(record, all_records):
    for element in all_records:
        if element["id"] == str(record["id"]):
            element["title"] = record["title"]
            element["message"] = record["message"]
            element["image"] = record["image"]
            element["submission_time"] = util.get_new_timestamp()


def edit_answer(record, all_records):
    for element in all_records:
        if element["id"] == str(record["id"]):
            element["message"] = record["message"]
            element["image"] = record["image"]
            element["submission_time"] = util.get_new_timestamp()


def delete_record_from_file(record_id, option):
    all_records = read_all_items_from_file_by_option(option)
    all_records.pop(int(record_id))
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


def get_headers_by_option(option):
    if option == "questions":
        return QUESTION_HEADERS
    return ANSWER_HEADERS


def get_file_path(option="answers"):
    if option == "answers":
        return ANSWER_FILE_PATH
    return QUESTION_FILE_PATH


def update_vote_number(option, id, vote_direction):
    vote_dic = {"up":1, "down": -1}
    all_records = get_dict_list_from_csv_file(option)
    for record in all_records:
        if record["id"] == id:
            if int(record["vote_number"]) != 0:
                record["vote_number"] = int(record["vote_number"]) + vote_dic[vote_direction]
            break
    save_to_file(all_records, option)
