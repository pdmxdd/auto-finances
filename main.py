from utils.csv import delete_file, write_dict_list
from transactions.chase import chase_message_to_dict
from gmail.messages import get_message, get_message_ids_by_query
from gmail.service import get_service
from gmail.labels import get_labels_dict

if __name__ == '__main__':
    service = get_service()
    labels_dict = get_labels_dict(service)
    
    csv_filepath = './expenses.csv'

    # for manual testing purposes only:
    delete_file(csv_filepath)

    chase_messages = [get_message(message_id['id'], service) for message_id in get_message_ids_by_query('from:"paul@paulmatthews.dev" subject:"Your Single Transaction Alert From Chase"', service)]

    write_dict_list(csv_filepath, [chase_message_to_dict(message) for message in chase_messages])

    # for message in chase_messages: 
    #   remove_labels_from_message(message['id], [labels_dict['INBOX'], labels_dict['UNREAD']], service)
    #   add_labels_to_message(message['id], [labels_dict["Auto-Finances/Recorded"], labels_dict["Auto-Finances/Transaction/Chase"]], service)

    # TODO: all of the pieces of the MVP exist. time to pull it all together and manually test it out
