from chase_transactions import chase_message_to_dict
from gmail_messages import get_message, get_message_ids_by_query
from gmail_service import get_service
from gmail_labels import get_labels_dict




if __name__ == '__main__':
    service = get_service()
    labels_dict = get_labels_dict(service)
    
    chase_messages = [get_message(message_id['id'], service) for message_id in get_message_ids_by_query('from:"paul@paulmatthews.dev" subject:"Your Single Transaction Alert From Chase"', service)]

    for message in chase_messages:
        print("chase_message_dict: {}".format(chase_message_to_dict(message)))

        # TODO: write chase_dict to CSV

        # TODO: update chase message labels (remove INBOX & UNREAD; add Auto-Finances/Transaction/Chase & Auto-Finances/Recorded)
