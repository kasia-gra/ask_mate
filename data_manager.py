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
def get_all_records(cursor: RealDictCursor, table: str):
    cursor.execute(f"""
                    SELECT *
                    FROM {table};
                    """)
    return cursor.fetchall()


def add_record(new_record, option):
    if option == "question":
        add_question(new_record)
    elif option == "answer":
        add_answer(new_record)
    else:
        add_comment(new_record)


@connection.connection_handler
def add_question(cursor: RealDictCursor, new_record: dict):
    if new_record["image"]:
        new_path = new_record["image"]
    else:
        new_path = ""
    cursor.execute(f"""
                    INSERT INTO question
                        (title, message, image, vote_number, view_number)
                    VALUES
                        (%(title)s, %(message)s, %(img_path)s, 0, 0);
                    """, {
                        'title': new_record["title"],
                        'message': new_record["message"],
                        'img_path': new_path
                        })


@connection.connection_handler
def add_answer(cursor: RealDictCursor, new_record: dict):
    if new_record["image"]:
        new_path = new_record["image"]
    else:
        new_path = ""
    cursor.execute("""
                    INSERT INTO answer
                        (message, image, vote_number)
                    VALUES
                        (%(title)s, %(message)s, %(img_path)s, 0);
                    """, {
                        'message': new_record["message"],
                        'img_path': new_path
                        })


@connection.connection_handler
def add_comment(cursor: RealDictCursor, new_record: dict):
    pass


def edit_record(new_record, option):
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
                        submission_time = CURRENT_TIMESTAMP
                    WHERE id = %(id)s;
                    """, {
                        'title': new_record["title"],
                        'message': new_record["message"],
                        'img_path': new_record["image"],
                        'id': int(new_record["id"])})


@connection.connection_handler
def edit_answer(cursor: RealDictCursor, new_record: dict):
    cursor.execute(f"""
                    UPDATE answer
                    SET
                        title = %(title)s,
                        message = %(message)s,
                        image = %(img_path)s,
                        submission_time = CURRENT_TIMESTAMP
                    WHERE id = %(id)s;
                    """, {
                        'message': new_record["message"],
                        'img_path': new_record["image"],
                        'id': int(new_record["id"])})


@connection.connection_handler
def edit_comment(cursor: RealDictCursor, new_record: dict):
    pass


def delete_record(record_id, option):
    if option == "question":
        delete_question(record_id)
    elif option == "answer":
        delete_answer(record_id)
    else:
        delete_comment(record_id)


@connection.connection_handler
def delete_question(cursor: RealDictCursor, record_id: int):
    cursor.execute(f"""
                    DELETE FROM question
                    WHERE id = %(id)s;
                    """, {'id': record_id})


@connection.connection_handler
def delete_answer(cursor: RealDictCursor, record_id: int):
    cursor.execute(f"""
                    DELETE FROM answer
                    WHERE id = %(id)s;
                    """, {'id': record_id})


@connection.connection_handler
def delete_comment(cursor: RealDictCursor, record_id: int):
    pass


@connection.connection_handler
def get_specific_record(cursor: RealDictCursor, record_id: int, option: str):
    cursor.execute(f"SELECT * FROM {option} WHERE id = {record_id};")
    return cursor.fetchone()


def get_headers_by_option(option="question"):
    return ANSWER_HEADERS if option == "answer" else QUESTION_HEADERS


def get_file_path(option="answer"):
    return ANSWER_FILE_PATH if option == "answer" else QUESTION_FILE_PATH


@connection.connection_handler
def increase_view_number(cursor: RealDictCursor, question_id: int):
    cursor.execute(f"""
                UPDATE question
                SET view_number = view_number + 1
                WHERE id = %(id)s;
           """, {'id': question_id})

# def increase_view_number(question_id):
#     all_questions = read_all_items_from_file_by_option("question")
#     for question in all_questions:
#         if question["id"] == question_id:
#             question["view_number"] = str(int(question["view_number"]) + 1)
#     save_to_file(all_questions, "question")
#
#
# def update_vote_number(option, record_id, vote_direction):
#     vote_dic = {"up": 1, "down": -1}
#     all_records = get_dictionary_from_database(option)
#     for record in all_records:
#         if record["id"] == record_id:
#             record["vote_number"] = str(int(record["vote_number"]) + vote_dic[vote_direction])
#             break
#     save_to_file(all_records, option)
#
#
# def make_vote_for_question(question_id, result):
#     result.set_cookie("q" + question_id, "voted")
#     update_vote_number("question", question_id, "down")
#     return result
