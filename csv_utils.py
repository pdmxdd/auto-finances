# QUICKFIX: yoinked from another project I've worked on. It's messy, but will allow me to move forward quickly. will need to come back and find a better solution for working with CSVs, if I continue to go the flat-file route.

from csv import DictReader, DictWriter
import os

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

def create_csv_and_write_dict_list(filepath, write_dict_list):
    with open(filepath, 'w', newline='\n') as csv_file:
        writer = DictWriter(csv_file, fieldnames=write_dict_list[0].keys())

        writer.writeheader()

        writer.writerows(write_dict_list)

    return "file written to {}".format(filepath)

def write_csv(filepath, columns, data):
    with open(filepath, 'w', newline='\n') as csv_file:
        writer = DictWriter(csv_file, fieldnames=columns)
        
        writer.writeheader()

        writer.writerows(data)
    
    return "file written to {}".format(filepath)

def delete_row_from_csv(filepath, row_number):
    current_data = read_csv(filepath)
    print(current_data)
    # recreate current_data - row_number
    overwritten_data = []
    for i, order in enumerate(current_data):
        if(i != row_number):
            overwritten_data.append(order)
        # if(i == row_number):
        #     print("i: {}\nrow_number: {}\nrow: {}".format(i, row_number, order))
    write_csv(filepath, overwritten_data[0].keys(), overwritten_data)


def write_row_to_csv(filepath, row):
    with open(filepath, 'a', newline='\n') as csv_file:
        DictWriter(csv_file, fieldnames=row.keys()).writerow(row)

    return "row added to {}".format(filepath)

def delete_row(row_number):
    print("about to delete: {}\nfrom: {}".format(row_number, 'reports/pending_orders/buy_orders.csv'))
    delete_row_from_csv('reports/pending_orders/buy_orders.csv', row_number)

def delete_rows(row_numbers):
    print("about to delete: {}".format(row_numbers))
    for row_number in row_numbers:
        delete_row(row_number)