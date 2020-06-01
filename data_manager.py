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


def format_dictionary_data():
    dicts_list = get_dictionary_from_database("question")
    # for dictionary in dicts_list:
    #     for key, value in dictionary.items():
    #         if key in NUMERICAL_VALUE_HEADERS:
    #             dictionary[key] = int(value)
    #         elif key in DATE_HEADERS:
    #             dictionary[key] = datetime.utcfromtimestamp(int(value)).strftime('%Y-%m-%d %H:%M:%S')
    return dicts_list


@connection.connection_handler
def get_dictionary_from_database(cursor: RealDictCursor, table: str):
    cursor.execute(f"SELECT * FROM {table};")
    return cursor.fetchall()


def add_record_to_file(new_record, option):
    if option == "question":
        add_question(new_record)
    elif option == "answer":
        add_answer(new_record)
    else:
        add_comment(new_record)


@connection.connection_handler
def add_question(cursor: RealDictCursor, new_record: dict):
    cursor.execute("""
                    INSERT INTO question
                        (title, message, image, vote_number, view_number, submission_time)
                    VALUES
                        (%(title)s, %(message)s, %(img_path)s, 0, 0, %(timestamp)s);
                    """, {
                        'title': new_record["title"],
                        'message': new_record["message"],
                        'img_path': new_record["image"],
                        'timestamp': util.get_new_timestamp()})


@connection.connection_handler
def add_answer(cursor: RealDictCursor, new_record: dict):
    cursor.execute("""
                    INSERT INTO answer
                        (message, image, vote_number, submission_time)
                    VALUES
                        (%(title)s, %(message)s, %(img_path)s, 0, %(timestamp)s);
                    """, {
                        'message': new_record["message"],
                        'img_path': new_record["image"],
                        'timestamp': util.get_new_timestamp()})


@connection.connection_handler
def add_comment(cursor: RealDictCursor, new_record: dict):
    pass


def edit_record_in_file(new_record, option):
    if option == "question":
        edit_question(new_record)
    elif option == "answer":
        edit_answer(new_record)
    else:
        edit_comment(new_record)


@connection.connection_handler
def edit_question(cursor: RealDictCursor, new_record: dict):
    cursor.execute(f"""
                    UPDATE question
                    SET
                        title = %(title)s,
                        message = %(message)s,
                        image = %(img_path)s,
                        submission_time = %(timestamp)s
                    WHERE id = %(id)s;
                    """, {
                        'title': new_record["title"],
                        'message': new_record["message"],
                        'img_path': new_record["image"],
                        'timestamp': util.get_new_timestamp()})


@connection.connection_handler
def edit_answer(cursor: RealDictCursor, new_record: dict):
    cursor.execute(f"""
                    UPDATE answer
                    SET
                        title = %(title)s,
                        message = %(message)s,
                        image = %(img_path)s,
                        submission_time = %(timestamp)s
                    WHERE id = %(id)s;
                    """, {
                        'message': new_record["message"],
                        'img_path': new_record["image"],
                        'timestamp': util.get_new_timestamp()})


@connection.connection_handler
def edit_comment(cursor: RealDictCursor, new_record: dict):
    pass


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
    return get_dictionary_from_database(option)


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
    all_records = get_dictionary_from_database(option)
    for record in all_records:
        if record["id"] == record_id:
            record["vote_number"] = str(int(record["vote_number"]) + vote_dic[vote_direction])
            break
    save_to_file(all_records, option)


def make_vote_for_question(question_id, result):
    result.set_cookie("q" + question_id, "voted")
    update_vote_number("question", question_id, "down")
    return result
