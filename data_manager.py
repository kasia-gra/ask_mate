from datetime import datetime
import os
import util
import csv

from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import connection

dir_path = os.path.dirname(__file__)
ANSWER_FILE_PATH = os.path.join(dir_path, "sample_data/answer.csv")
QUESTION_FILE_PATH = os.path.join(dir_path, "sample_data/question.csv")
QUESTION_HEADERS = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
ANSWER_HEADERS = ["id", "submission_time", "vote_number", "question_id", "message", "image"]
UPLOAD_FOLDER = os.path.join(dir_path, "static/img/")
NUMERICAL_VALUE_HEADERS = ["id", "view_number", "vote_number", "question_id"]
DATE_HEADERS = ["submission_time"]


@connection.connection_handler
def get_dict_list_from_csv_file(cursor: RealDictCursor, option: str):
    option = option.replace("'", "")
    cursor.execute("""
                        SELECT *
                        FROM %(table_name_option);
                        """, {'table_name_option': option})
    return cursor.fetchall()


# def get_dict_list_from_csv_file(option):
#     dicts_list = []
#     filepath = get_file_path(option)
#     with open(filepath, "r") as csvfile:
#         reader = csv.DictReader(csvfile, fieldnames=get_headers_by_option(option))
#         for dictionary in reader:
#             dicts_list.append(dictionary)
#     return dicts_list


def save_to_file(all_records, option):
    with open(get_file_path(option), "w", newline="") as file:
        data = csv.DictWriter(file, fieldnames=get_headers_by_option(option))
        for element in all_records:
            data.writerow(element)


def format_dictionary_data():
    dicts_list = get_dict_list_from_csv_file("question")[1::]
    for dictionary in dicts_list:
        for key, value in dictionary.items():
            if key in NUMERICAL_VALUE_HEADERS:
                dictionary[key] = int(value)
            elif key in DATE_HEADERS:
                dictionary[key] = datetime.utcfromtimestamp(int(value)).strftime('%Y-%m-%d %H:%M:%S')
    return dicts_list


def add_record_to_file(new_record, option):
    all_records = read_all_items_from_file_by_option(option)
    if option == "question":
        add_question(new_record)
    else:
        add_answer(new_record)
    all_records.append(new_record)
    save_to_file(all_records, option)


def add_question(new_record):
    new_record["id"] = util.get_latest_id("question")
    new_record["submission_time"] = util.get_new_timestamp()
    new_record["view_number"] = 0
    new_record["vote_number"] = 0


def add_answer(new_record):
    new_record["id"] = util.get_latest_id("answer")
    new_record["submission_time"] = util.get_new_timestamp()
    new_record["vote_number"] = 0


def edit_record_in_file(record, option):
    all_records = read_all_items_from_file_by_option(option)
    if option == "question":
        edit_question(record, all_records)
        save_to_file(all_records, option)


def edit_question(record, all_records):
    for element in all_records:
        if element["id"] == str(record["id"]):
            element["title"] = record["title"]
            element["message"] = record["message"]
            element["image"] = record["image"]
            element["submission_time"] = util.get_new_timestamp()


def delete_question_from_file(record_id):
    all_questions = read_all_items_from_file_by_option("question")
    for question in all_questions:
        if question["id"] == record_id:
            index_of_question = all_questions.index(question)
            util.remove_question_image_with_answer_images(question["id"], question["image"])
    all_questions.pop(index_of_question)
    save_to_file(all_questions, "question")


def delete_answer_from_file(record_id):
    all_answers = read_all_items_from_file_by_option("answer")
    for answer in all_answers:
        if answer["id"] == record_id:
            index_of_question = all_answers.index(answer)
            util.remove_answer_image(answer["question_id"], answer["image"])
    all_answers.pop(index_of_question)
    save_to_file(all_answers, "answer")


def read_all_items_from_file_by_option(option="question"):
    if option == "question":
        return get_dict_list_from_csv_file("question")
    return get_dict_list_from_csv_file("answer")


def get_old_record(record_id, option):
    all_records = read_all_items_from_file_by_option(option)
    for element in all_records:
        if record_id == element["id"]:
            return element


def get_headers_by_option(option="question"):
    return ANSWER_HEADERS if option == "answer" else QUESTION_HEADERS


def get_file_path(option="answer"):
    return ANSWER_FILE_PATH if option == "answer" else QUESTION_FILE_PATH


def increase_view_number(question_id):
    all_questions = read_all_items_from_file_by_option("question")
    for question in all_questions:
        if question["id"] == question_id:
            question["view_number"] = str(int(question["view_number"]) + 1)
    save_to_file(all_questions, "question")


def update_vote_number(option, record_id, vote_direction):
    vote_dic = {"up": 1, "down": -1}
    all_records = get_dict_list_from_csv_file(option)
    for record in all_records:
        if record["id"] == record_id:
            record["vote_number"] = str(int(record["vote_number"]) + vote_dic[vote_direction])
            break
    save_to_file(all_records, option)


def make_vote_for_question(question_id, result):
    result.set_cookie("q" + question_id, "voted")
    update_vote_number("question", question_id, "down")
    return result
