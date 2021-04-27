from csv_utils import delete_file, write_dict_list
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

    # TODO: update chase message labels (remove INBOX & UNREAD; add Auto-Finances/Transaction/Chase & Auto-Finances/Recorded) -> after a message is recorded it needs to have labels added and removed. will need to chop up the list comprehensions
