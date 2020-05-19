import data_manager
from datetime import datetime

NUMERICAL_VALUE_HEADERS = ["id", "view_number", "vote_number", "question_id"]
DATE_HEADERS = ["submission_time"]


def format_dictionary_data():
    dicts_list = data_manager.get_dict_list_from_csv_file("questions")[1::]
    for dictionary in dicts_list:
        for key, value in dictionary.items():
            if key in NUMERICAL_VALUE_HEADERS:
                dictionary[key] = int(value)
            elif key in DATE_HEADERS:
                dictionary[key] = datetime.utcfromtimestamp(int(value)).strftime('%Y-%m-%d %H:%M:%S')
    return dicts_list


def sort_dictionary(dicts_list, sort_by):
    criteria_and_order_list = sort_by.split("-")
    criteria = criteria_and_order_list[0]
    order = criteria_and_order_list[1]
    order_sort = {"desc": 1, "asc": 0}
    dicts_list.sort(key=lambda dictionary: dictionary[criteria], reverse=order_sort[order])
    return dicts_list
