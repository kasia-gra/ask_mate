import data_manager
from datetime import datetime

NUMERICAL_VALUE_HEADERS = ["id", "view_number", "vote_number", "question_id"]
DATE_HEADERS = ["submission_time"]

def format_dictionary_data():
    dicts_list = data_manager.get_dict_list_from_csv_file()
    for dictionary in dicts_list:
        for key, value in dictionary.items():
            if key in NUMERICAL_VALUE_HEADERS:
                dictionary[key] = int(value)
            elif key in DATE_HEADERS:
                dictionary[key] = datetime.utcfromtimestamp(int(value)).strftime('%Y-%m-%d %H:%M:%S')
    return dicts_list


def sort_dictionary(sort_by, dicst_list):
    dicst_list.sort(key=lambda dictionary: dictionary[sort_by], reverse=True)
    return dicst_list

