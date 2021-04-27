# QUICKFIX: yoinked from another project I've worked on. It's messy, but will allow me to move forward quickly. will need to come back and find a better solution for working with CSVs, if I continue to go the flat-file route.

import os
from csv import DictReader, DictWriter

transaction_write_list = [
    "gmail_message_id",
    "gmail_thread_id",
    "authorized_time",
    "amount",
    "vendor",
    "account",
    "condensed_message",
    "Subject",
    "From",
    "To",
    "Date"
]

def read_csv(filepath):
    data = []
    with open(filepath, 'r', newline='\n') as csv_file:
        reader = DictReader(csv_file)
        for row in reader:
            # print("row: {}".format(row))
            data.append(row)

    return data

def delete_file(filepath):
    if os.path.exists(filepath) and os.path.isfile(filepath):
        os.remove(filepath)
    else:
        return "{} did not exist in local directory".format(filepath)
    return "removed {} from local directory".format(filepath)

def write_dict_list(filepath, write_dict_list):
    if not os.path.exists(filepath):
        with open(filepath, 'w', newline='\n') as csv_file:
            writer = DictWriter(csv_file, fieldnames=transaction_write_list)

            writer.writeheader()

            writer.writerows(write_dict_list)
    else:
        with open(filepath, 'a', newline='\n') as csv_file:
            writer = DictWriter(csv_file, fieldnames=transaction_write_list)
            writer.writerows(write_dict_list)

    return "file written to {}".format(filepath)
