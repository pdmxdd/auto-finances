from utils.aws import upload_file_to_bucket
from transactions.discover import discover_message_to_dict
from utils.csv import write_dict_list
from transactions.chase import chase_message_to_dict
from gmail.messages import add_labels_to_message, get_message, get_message_ids_by_query, remove_labels_from_message
from gmail.service import get_service
from gmail.labels import get_labels_dict

def scan_record_update_chase_transactions(service, csv_filepath, labels_dict):
    CHASE_QUERY = 'from:"no.reply.alerts@chase.com" subject:"Your Single Transaction Alert from Chase" label:"INBOX" label:"UNREAD"'
    chase_messages = [get_message(message_id['id'], service) for message_id in 
    get_message_ids_by_query(CHASE_QUERY, service)]

    for chase_message in chase_messages:
        message_dict = chase_message_to_dict(chase_message)
        write_dict_list(csv_filepath, [message_dict])
        print("wrote condensed_message: {}".format(message_dict['condensed_message']))
        add_labels_to_message(chase_message['id'], [labels_dict['Auto-Finances/Recorded'], labels_dict['Auto-Finances/Transaction/Chase']], service)
        print("Auto-Finances/Recorded & Auto-Finances/Transaction/Chase labels added")
        remove_labels_from_message(chase_message['id'], [labels_dict['INBOX'], labels_dict['UNREAD']], service)
        print("INBOX & UNREAD labels removed")

def scan_record_update_discover_transactions(service, csv_filepath, labels_dict):
    DISCOVER_QUERY = 'from:"discover" subject:"Transaction Alert" label:"INBOX" label:"UNREAD"'
    discover_messages = [get_message(message_id['id'], service) for message_id in get_message_ids_by_query(DISCOVER_QUERY, service)]

    for discover_message in discover_messages:
        message_dict = discover_message_to_dict(discover_message)
        write_dict_list(csv_filepath, [message_dict])
        add_labels_to_message(discover_message['id'], [labels_dict['Auto-Finances/Recorded'], labels_dict['Auto-Finances/Transaction/Discover']], service)
        remove_labels_from_message(discover_message['id'], [labels_dict['INBOX'], labels_dict['UNREAD']], service)

if __name__ == '__main__':
    service = get_service()
    labels_dict = get_labels_dict(service)
    
    csv_filepath = './expenses.csv'

    scan_record_update_chase_transactions(service, csv_filepath, labels_dict)

    scan_record_update_discover_transactions(service, csv_filepath, labels_dict)

    bucket_name = 'auto-finances'

    upload_file_to_bucket(bucket_name, csv_filepath)