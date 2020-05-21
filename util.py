from datetime import datetime
import data_manager
import os
import glob
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def get_new_timestamp():
    now = datetime.now()
    return str(datetime.timestamp(now))[:10:]


def get_latest_id(option="questions"):
    all_records = data_manager.read_all_items_from_file_by_option(option)
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
        name_options = {"questions": "q", "answers": "a"}
        filename = name_options[option] + "_" + get_latest_id(option) + "_" + secure_filename(file.filename)
        if option == "answers":
            upload_folder = os.path.join(upload_folder, folder_id)
            if not os.path.exists(upload_folder):
                os.mkdir(upload_folder)
        file.save(os.path.join(upload_folder, filename))
        return str(filename)


def sort_dictionary(dicts_list, sort_by):
    criteria_and_order_list = sort_by.split("-")
    criteria = criteria_and_order_list[0]
    order = criteria_and_order_list[1]
    order_sort = {"desc": 1, "asc": 0}
    dicts_list.sort(key=lambda dictionary: dictionary[criteria], reverse=order_sort[order])
    return dicts_list


def remove_answer_image(question_id, image_name):
    if os.path.exists(data_manager.UPLOAD_FOLDER + image_name) and image_name != "":
        file_path = data_manager.UPLOAD_FOLDER + question_id + "/" + image_name
        os.remove(file_path)


def remove_question_image_with_answer_images(question_id, image_name):
    if image_name != "":
        file_path = data_manager.UPLOAD_FOLDER + image_name
        os.remove(file_path)
    all_images_in_folder = glob.glob(data_manager.UPLOAD_FOLDER + question_id + "/*")
    for image in all_images_in_folder:
        os.remove(image)
    folder_path = data_manager.UPLOAD_FOLDER + question_id
    os.rmdir(folder_path)
