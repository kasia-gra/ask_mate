import os
from psycopg2.extras import RealDictCursor
import connection

dir_path = os.path.dirname(__file__)
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
    if criteria_and_direction[0] in QUESTION_HEADERS and criteria_and_direction[1] in ['ASC', 'DESC']:
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
    cursor.execute("""
                    SELECT *
                    FROM answer
                    WHERE question_id = %(q_id)s;
                    """, {'q_id': question_id})
    return cursor.fetchall()


@connection.connection_handler
def count_answers_for_question(cursor: RealDictCursor, question_id: int):
    cursor.execute("""
                        SELECT COUNT(*)
                        FROM answer
                        WHERE question_id = %(q_id)s;
                        """, {'q_id': question_id})
    return cursor.fetchone()


def add_record(new_record, option):
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
                        (title, message, image, submission_time, user_id, vote_number, view_number)
                    VALUES
                        (%(title)s, %(message)s, %(img_path)s, %(submission_time)s, %(user_id)s, 0, 0);
                    """, {
        'title': new_record["title"],
        'message': new_record["message"],
        'submission_time': new_record["submission_time"],
        'img_path': new_record["image"],
        'user_id': new_record["user_id"]
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
    (question_id, answer_id, message, submission_time, edited_number, user_id)
    VALUES (%s, %s, %s, %s, %s, %s);
    """
    cursor.execute(query, (new_record["question_id"], new_record["answer_id"],
                           new_record["message"], new_record["submission_time"], new_record["edited_number"], new_record["user_id"]))


def edit_record(new_record, option):
    if option == "question":
        edit_question(new_record)
    elif option == "answer":
        edit_answer(new_record)
    else:
        edit_comment(new_record)


@connection.connection_handler
def edit_question(cursor: RealDictCursor, new_record: dict):
    cursor.execute("""
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
    cursor.execute("""
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
    query = """
    UPDATE comment
    SET message = %s, submission_time = %s, edited_number = %s
    WHERE id = %s
    """
    cursor.execute(query, (new_record.get("message"), new_record.get("submission_time"),
                           new_record.get("edited_number"), new_record.get("id")))


def delete_record(record_id, option):
    if option == "question":
        delete_question(record_id)
    elif option == "answer":
        delete_answer(record_id)
    else:
        delete_comment(record_id)


@connection.connection_handler
def delete_question(cursor: RealDictCursor, record_id: int):
    cursor.execute("""
                    DELETE FROM question
                    WHERE id = %(id)s;
                    """, {'id': record_id})


@connection.connection_handler
def delete_answer(cursor: RealDictCursor, record_id: int):
    cursor.execute("""
                    DELETE FROM answer
                    WHERE id = %(id)s;
                    """, {'id': record_id})


@connection.connection_handler
def delete_comment(cursor: RealDictCursor, record_id: int):
    cursor.execute("""
                    DELETE FROM comment
                    WHERE id = %(id)s;
                    """, {'id': record_id})


@connection.connection_handler
def delete_connected_comment(cursor: RealDictCursor, question_id: int = -1, answer_id: int = -1):
    cursor.execute("""
                    DELETE FROM comment
                    WHERE question_id = %(qid)s AND answer_id IS NULL OR answer_id = %(aid)s AND question_id IS NULL;
                    """, {'qid': question_id, 'aid': answer_id})


@connection.connection_handler
def delete_tag(cursor: RealDictCursor, question_id: int, tag_id: int):
    cursor.execute("""
                    DELETE FROM question_tag
                    WHERE question_id = %(question_id)s AND tag_id = %(tag_id)s;
                    """, {'question_id': question_id, 'tag_id': tag_id})


@connection.connection_handler
def delete_connected_tags(cursor: RealDictCursor, question_id: int):
    cursor.execute("""
                        DELETE FROM question_tag
                        WHERE question_id = %(question_id)s;
                        """, {'question_id': question_id})


@connection.connection_handler
def get_question_comments(cursor: RealDictCursor, question_id: int):
    query = """
    SELECT id, submission_time, message, edited_number from comment
    WHERE question_id = %s
    """
    cursor.execute(query, (question_id,))
    return cursor.fetchall()


@connection.connection_handler
def get_answers_comments(cursor: RealDictCursor, answers_id_list: list):
    answers_id = ", ".join(str(id) for id in answers_id_list)
    query = f"""
    SELECT id, answer_id, submission_time, message, edited_number from comment
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


@connection.connection_handler
def search_for_phrase_questions(cursor: RealDictCursor, search_phrase: str):
    cursor.execute(f"""
                SELECT DISTINCT question.*
                FROM question
                FULL OUTER JOIN answer
                ON question.id = answer.question_id
                WHERE question.message ILIKE %(phrase)s
                OR question.title ILIKE %(phrase)s
                OR answer.message ILIKE %(phrase)s;
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
def get_available_tags(cursor: RealDictCursor):
    cursor.execute(f"""
                SELECT *
                FROM tag;
           """)
    return cursor.fetchall()


@connection.connection_handler
def get_questions_with_specific_tag(cursor: RealDictCursor, tag: str):
    cursor.execute("""
                SELECT *
                FROM question
                LEFT JOIN question_tag
                    ON question.id = question_tag.question_id
                LEFT JOIN tag
                    ON question_tag.tag_id = tag.id
                WHERE tag.name = %(tag)s;
           """, {'tag': tag})
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


def is_tag_already_assigned(question_id, tag_id):
    tag_assigned = False
    question_tags = get_tags_for_questions(question_id)
    for dictionary in question_tags:
        if dictionary["tag_id"] == tag_id:
            tag_assigned = True
            break
    return tag_assigned


@connection.connection_handler
def assign_tag_to_question(cursor: RealDictCursor, question_id: int, tag_id: int):
    cursor.execute(f"""
                INSERT INTO question_tag 
                VALUES (%s, %s);
           """, (question_id, tag_id))


@connection.connection_handler
def add_user(cursor: RealDictCursor, user_dict: dict):
    cursor.execute("""
                    INSERT INTO users
                        (email, password, registration_time, reputation)
                    VALUES
                        (%(email)s, %(password)s, %(registration_time)s, %(reputation)s);
                    """, {
        'email': user_dict["email"],
        'password': user_dict["password"],
        'registration_time': user_dict["registration_time"],
        'reputation': user_dict["reputation"]
    })


@connection.connection_handler
def get_password(cursor: RealDictCursor, email: str):
    cursor.execute(f"""
                    SELECT password
                    FROM users
                    WHERE email = (%(email)s);
               """, {'email': email})
    return cursor.fetchone()


@connection.connection_handler
def update_reputation(cursor: RealDictCursor, user_id: int, amount: int):
    cursor.execute("""
                UPDATE users
                SET reputation = reputation + %(amount)s
                WHERE id = %(id)s;
           """, {'id': user_id, 'amount': amount})


@connection.connection_handler
def get_user_id(cursor: RealDictCursor, email: str):
    cursor.execute(f"""
                    SELECT id
                    FROM users
                    WHERE email = (%(email)s);
               """, {'email': email})
    return cursor.fetchone()


@connection.connection_handler
def get_users(cursor: RealDictCursor):
    query = """
    SELECT u.id, u.email, u.registration_time, u.reputation, COUNT(DISTINCT q.*) AS questions_number, COUNT(DISTINCT a.*) AS answers_number, COUNT(DISTINCT c.*) AS comments_number
    FROM users u LEFT JOIN question q ON u.id = q.user_id LEFT JOIN answer a ON q.user_id = a.user_id LEFT JOIN comment c ON u.id = c.user_id
    GROUP BY u.id ORDER BY u.id;
    """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_user_by_id(cursor: RealDictCursor, user_id: int):
    query = """
    SELECT u.id, u.email, u.registration_time, u.reputation, COUNT(DISTINCT q.*) AS questions_number, COUNT(DISTINCT a.*) AS answers_number, COUNT(DISTINCT c.*) AS comments_number
    FROM users u LEFT JOIN question q ON u.id = q.user_id LEFT JOIN answer a ON q.user_id = a.user_id LEFT JOIN comment c ON u.id = c.user_id
    WHERE u.id = %(user_id)s GROUP BY u.id ORDER BY u.id;
    """
    cursor.execute(query, {"user_id": user_id})
    return cursor.fetchone()


@connection.connection_handler
def get_questions_by_user_id(cursor: RealDictCursor, user_id: int):
    query = """
    SELECT id, submission_time, view_number, vote_number, title, message, image, user_id
    FROM question
    WHERE user_id = %(user_id)s
    ORDER BY id
    """
    cursor.execute(query, {'user_id': user_id})
    return cursor.fetchall()


@connection.connection_handler
def get_answers_by_user_id(cursor: RealDictCursor, user_id: int):
    query = """
    SELECT id, submission_time, vote_number, question_id, message, image, user_id
    FROM answer
    WHERE user_id = %(user_id)s
    ORDER BY id
    """
    cursor.execute(query, {'user_id': user_id})
    return cursor.fetchall()


@connection.connection_handler
def get_comments_by_user_id(cursor: RealDictCursor, user_id: int):
    query = """
    SELECT id, question_id, answer_id, message, submission_time, edited_number, user_id
    FROM comment
    WHERE user_id = %(user_id)s
    ORDER BY id
    """
    cursor.execute(query, {'user_id': user_id})
    return cursor.fetchall()


@connection.connection_handler
def get_question_owner_based_on_answer(cursor: RealDictCursor, answer_id: int):
    query = """
    SELECT question.user_id
    FROM question JOIN answer ON question.id = answer.question_id
    WHERE answer.id = %(answer_id)s
    """
    cursor.execute(query, {'answer_id': answer_id})
    return cursor.fetchone()

@connection.connection_handler
def change_answer_status(cursor: RealDictCursor, answer_id: int, status=bool):
    query = f"""
    UPDATE answer
    SET accepted = {status}
    WHERE id = %(answer_id)s
    """
    cursor.execute(query, {'answer_id': answer_id})
