@connection.connection_handler
def get_data_from_user_by_option(cursor: RealDictCursor, user_id: int, option: str):
    if option in ['question', 'answer', 'comment']:
        query = """
            SELECT *
            FROM {option}
            WHERE user_id = %(user_id)s
            ORDER BY id
            """
        cursor.execute(query, {'user_id': user_id})
        return cursor.fetchall()

==>


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


---------------------------------------------------


@connection.connection_handler
def get_user_data(cursor: RealDictCursor, email: str):
    cursor.execute(f"""
                        SELECT *
                        FROM users
                        WHERE email = (%(email)s);
                   """, {'email': email})
    return cursor.fetchone()


===>


@connection.connection_handler
def get_password(cursor: RealDictCursor, email: str):
    cursor.execute(f"""
                    SELECT password
                    FROM users
                    WHERE email = (%(email)s);
               """, {'email': email})
    return cursor.fetchone()


@connection.connection_handler
def get_user_id(cursor: RealDictCursor, email: str):
    cursor.execute(f"""
                    SELECT id
                    FROM users
                    WHERE email = (%(email)s);
               """, {'email': email})
    return cursor.fetchone()