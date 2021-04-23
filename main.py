from gmail_labels import get_labels_dict
from gmail_messages import get_message_ids_by_query, get_message, trim_headers, decode_message_part




if __name__ == '__main__':
    labels_dict = get_labels_dict()
    print("labels dict: {}".format(labels_dict))
    message_ids = get_message_ids_by_query('from:"chase" subject:"Your Single Transaction Alert from Chase" label:"INBOX" label:"UNREAD"')
    example_message = get_message(message_ids[0]['id'])
    print("example_message: {}".format(example_message))
    print("decoded message: {}".format(decode_message_part(example_message['payload'])))
    relevant_headers = trim_headers(example_message['payload']['headers'])
    print("relevant headers: {}".format(relevant_headers))