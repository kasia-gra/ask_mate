import data_manager
import csv


def get_dict_list_from_csv_file(option):
    dicts_list = []
    filepath = data_manager.get_file_path(option)
    with open(filepath, "r") as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=data_manager.get_headers_by_option(option))
        for dictionary in reader:
            dicts_list.append(dictionary)
    return dicts_list


def save_to_file(all_records, option):
    with open(data_manager.get_file_path(option), "w", newline="") as file:
        data = csv.DictWriter(file, fieldnames=data_manager.get_headers_by_option(option))
        for element in all_records:
            data.writerow(element)
