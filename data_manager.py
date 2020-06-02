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


@connection.connection_handler
def get_sorted_questions(cursor: RealDictCursor, criteria_and_direction):
    cursor.execute(f"""
                    SELECT *
                    FROM question
                    ORDER BY {criteria_and_direction[0]} {criteria_and_direction[1]};
                    """)
    return cursor.fetchall()

@connection.connection_handler
def get_five_records(cursor: RealDictCursor, table: str):
    cursor.execute(f"""
                    SELECT *
                    FROM {table}
                    LIMIT 5;
                    """)
    return cursor.fetchall()


@connection.connection_handler
def get_answers_for_question(cursor: RealDictCursor, question_id: int):
    cursor.execute(f"""
                    SELECT *
                    FROM answer
                    WHERE question_id = %(q_id)s;
                    """, {'q_id': question_id})
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
    cursor.execute(f"""
                    INSERT INTO question
                        (title, message, image, submission_time, vote_number, view_number)
                    VALUES
                        (%(title)s, %(message)s, %(img_path)s, %(submission_time)s, 0, 0);
                    """, {
                        'title': new_record["title"],
                        'message': new_record["message"],
                        'submission_time': new_record["submission_time"],
                        'img_path': new_record["image"]
                        })


@connection.connection_handler
def add_answer(cursor: RealDictCursor, new_record: dict):
    cursor.execute("""
                    INSERT INTO answer
                        (question_id, message, image, submission_time, vote_number)
                    VALUES
                        (%(question_id)s, %(message)s, %(img_path)s, %(submission_time)s, 0);
                    """, {
                        'question_id': new_record['question_id'],
                        'message': new_record["message"],
                        'submission_time': new_record["submission_time"],
                        'img_path': new_record["image"]
                        })


@connection.connection_handler
def add_comment(cursor: RealDictCursor, new_record: dict):
    query = """
    INSERT INTO comment
    (question_id, answer_id, message, submission_time, edited_number)
    VALUES (%s, %s, %s, %s, %s);
    """
    cursor.execute(query, (new_record["question_id"], new_record["answer_id"],
                   new_record["message"], new_record["submission_time"], new_record["edited_number"]))


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
                        submission_time = %(submission_time)s
                    WHERE id = %(id)s;
                    """, {
                        'title': new_record["title"],
                        'message': new_record["message"],
                        'img_path': new_record["image"],
                        'submission_time': new_record["submission_time"],
                        'id': int(new_record["id"])})


@connection.connection_handler
def edit_answer(cursor: RealDictCursor, new_record: dict):
    cursor.execute(f"""
                    UPDATE answer
                    SET
                        message = %(message)s,
                        image = %(img_path)s,
                        submission_time = %(submission_time)s
                    WHERE id = %(id)s;
                    """, {
                        'message': new_record["message"],
                        'img_path': new_record["image"],
                        'submission_time': new_record["submission_time"],
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
    cursor.execute(f"""
                    DELETE FROM comment
                    WHERE id = %(id)s;
                    """, {'id': record_id})


@connection.connection_handler
def delete_connected_comment(cursor: RealDictCursor, question_id: int = -1, answer_id: int = -1):
    cursor.execute(f"""
                    DELETE FROM comment
                    WHERE question_id = %(qid)s AND answer_id IS NULL OR answer_id = %(aid)s AND question_id IS NULL;
                    """, {'qid': question_id, 'aid': answer_id})


@connection.connection_handler
def delete_tag(cursor: RealDictCursor, question_id: int, tag_id: int):
    cursor.execute(f"""
                    DELETE FROM question_tag
                    WHERE question_id = %(question_id)s AND tag_id = %(tag_id)s;
                    """, {'question_id': question_id, 'tag_id': tag_id})


@connection.connection_handler
def delete_connected_tags(cursor: RealDictCursor, question_id: int):
    cursor.execute(f"""
                        DELETE FROM question_tag
                        WHERE question_id = %(question_id)s;
                        """, {'question_id': question_id})


@connection.connection_handler
def get_question_comments(cursor: RealDictCursor, question_id: int):
    query = """
    SELECT submission_time, message, edited_number from comment
    WHERE question_id = %s
    """
    cursor.execute(query, (question_id,))
    return cursor.fetchall()


@connection.connection_handler
def get_answers_comments(cursor: RealDictCursor, answers_id_list: list):
    answers_id = ", ".join(str(id) for id in answers_id_list)
    query = f"""
    SELECT answer_id, submission_time, message, edited_number from comment
    WHERE answer_id IN ({answers_id})
    """
    cursor.execute(query)
    return cursor.fetchall()


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


@connection.connection_handler
def increase_edited_number(cursor: RealDictCursor, comment_id: int):
    cursor.execute(f"""
                UPDATE comment
                SET edited_number = edited_number + 1
                WHERE id = %(id)s;
           """, {'id': comment_id})


@connection.connection_handler
def get_tags_for_questions(cursor: RealDictCursor, question_id: int):
    cursor.execute(f"""
                    SELECT *
                    FROM question_tag
                    LEFT JOIN tag
                    ON question_tag.tag_id= tag.id
                    WHERE question_id = %(id)s;
               """, {'id': question_id})
    return cursor.fetchall()


@connection.connection_handler
def update_vote_number(cursor: RealDictCursor, option: str, record_id: int, vote_direction: str):
    vote_dic = {"up": 1, "down": -1}
    vote = vote_dic[vote_direction]
    cursor.execute(f"""
                UPDATE {option}
                SET vote_number = vote_number + {vote}
                WHERE id = %(id)s;
           """, {'id': record_id})


def make_vote_for_question(question_id, result):
    result.set_cookie("q" + question_id, "voted")
    update_vote_number("question", question_id, "down")
    return result


# @connection.connection_handler
# def search_for_phrase(cursor: RealDictCursor, search_phrase: str):
#     cursor.execute(f"""
#                 SELECT question.title, question.message, answer.message,
#                 FROM question
#                 FULL JOIN answer
#                 ON question.id = answer.question_id
#                 WHERE question.message ILIKE %(phrase)s OR question.title ILIKE %(phrase)s OR answer.message ILIKE %(phrase)s;
#            """, {'phrase': '%' + search_phrase + '%'})
#     return cursor.fetchall()


@connection.connection_handler
def search_for_phrase_questions(cursor: RealDictCursor, search_phrase: str):
    cursor.execute(f"""
                SELECT DISTINCT question.*
                FROM question
                FULL OUTER JOIN answer
                ON question.id = answer.question_id
                WHERE question.message ILIKE %(phrase)s OR question.title ILIKE %(phrase)s OR answer.message ILIKE %(phrase)s;
           """, {'phrase': '%' + search_phrase + '%'})
    return cursor.fetchall()

@connection.connection_handler
def search_for_phrase_answers(cursor: RealDictCursor, search_phrase: str):
    cursor.execute(f"""
                SELECT *
                FROM answer
                WHERE answer.message ILIKE %(phrase)s;
           """, {'phrase': '%' + search_phrase + '%'})
    return cursor.fetchall()


@connection.connection_handler
def add_tag_to_db(cursor: RealDictCursor, new_tag: str):
    cursor.execute(f"""
                INSERT INTO tag (name)
                VALUES (%(tag_name)s);
           """, {'tag_name': new_tag})


@connection.connection_handler
def get_tag_id(cursor: RealDictCursor, new_tag: str):
    cursor.execute(f"""
                SELECT id
                FROM tag
                WHERE name = (%(tag_name)s);
           """, {'tag_name': new_tag})
    return cursor.fetchone()


def check_if_tag_already_available(new_tag, tags_list):
    tag_in_db = False
    for dictionary in tags_list:
        if dictionary["name"] == new_tag:
            tag_in_db = True
            break
    return tag_in_db


@connection.connection_handler
def assign_tag_to_question(cursor: RealDictCursor, question_id: int, tag_id: int):
    cursor.execute(f"""
                INSERT INTO question_tag 
                VALUES (%s, %s);
           """, (question_id, tag_id))

