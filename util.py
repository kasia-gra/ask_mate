from flask import session, abort
import time
import datetime
import data_manager
import os
import glob
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def check_if_user_is_logged():
    if 'username' not in session:
        abort(401)


def check_if_user_is_owner(user_id, owners_id):
    if user_id != owners_id:
        abort(401)


def get_user_details_from_session():
    username = session['username']
    user_id = data_manager.get_user_id(username)['id']
    return username, user_id


def get_new_timestamp():
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    return now


def get_latest_id(option="questions"):
    all_records = data_manager.get_all_records(option)
    index_of_last_record = len(all_records) - 1
    if all_records[index_of_last_record]["id"] == "id":
        return 1
    last_records_id = all_records[index_of_last_record]["id"]
    return str(int(last_records_id) + 1)


def change_timestamp_to_date(timestamp):
    date = datetime.utcfromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
    return str(date)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_image(file, upload_folder, option, folder_id=None):
    if file and allowed_file(file.filename):
        name_options = {"question": "q", "answer": "a"}
        filename = str(name_options[option] + "_" + str(get_latest_id(option)) + "_" + secure_filename(file.filename))
        if option == "answer":
            upload_folder = os.path.join(upload_folder, folder_id)
            if not os.path.exists(upload_folder):
                os.mkdir(upload_folder)
        file.save(os.path.join(upload_folder, filename))
        return str(filename)


def sort_dictionary(dicts_list, sort_by):
    criteria_and_order_list = sort_by.split("-")
    criteria = criteria_and_order_list[0]
    order = criteria_and_order_list[1]
    order_sort = {"DESC": 1, "ASC": 0}
    dicts_list.sort(key=lambda dictionary: dictionary[criteria], reverse=order_sort[order])
    return dicts_list


def remove_answer_image(question_id, image_name):
    if image_name != "":
        file_path = data_manager.UPLOAD_FOLDER + question_id + "/" + image_name
        os.remove(file_path)


def remove_question_image_with_answer_images(question_id, image_name):
    if image_name != "":
        file_path = data_manager.UPLOAD_FOLDER + image_name
        if os.path.isfile(file_path):
            os.remove(file_path)
    all_images_in_folder = glob.glob(data_manager.UPLOAD_FOLDER + question_id + "/*")
    for image in all_images_in_folder:
        if os.path.isfile(image):
            os.remove(image)
    folder_path = data_manager.UPLOAD_FOLDER + question_id
    if os.path.isfile(folder_path):
        os.rmdir(folder_path)


def prepare_questions_to_display(all_questions):
    message_max_length = 800
    title_max_length = 53
    for record in all_questions:
        record["number_of_answers"] = data_manager.count_answers_for_question(record["id"])["count"]
        if len(record["title"]) >= title_max_length:
            record["title"] = record["title"][:title_max_length] + "..."
        if len(record["message"]) >= message_max_length:
            record["message"] = record["message"][:message_max_length] + "..."
    return all_questions


def prepare_message_to_display(records):
    message_max_length = 800
    for record in records:
        if len(record["message"]) >= message_max_length:
            record["message"] = record["message"][:message_max_length] + "..."
    return records
