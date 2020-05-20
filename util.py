from datetime import datetime
import data_manager
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def get_new_timestamp():
    now = datetime.now()
    return str(datetime.timestamp(now))[:10:]


def get_latest_id(option="questions"):
    all_records = data_manager.read_all_items_from_file_by_option(option)
    index_of_last_record = len(all_records) - 1
    last_records_id = all_records[index_of_last_record]["id"]
    return str(int(last_records_id) + 1)


def change_timestamp_to_date(timestamp):
    date = datetime.utcfromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
    return str(date)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_image(file, upload_folder):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(upload_folder, filename))
        return str(filename)
