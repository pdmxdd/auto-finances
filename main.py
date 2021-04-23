from __future__ import print_function
import base64

from gmail_service import get_service

def get_labels_dict():
    """
    Returns a dictionary of Gmail labels key: name value: id.
    """
    service = get_service()
    labels = service.users().labels().list(userId="me").execute()
    # print("labels: {}".format(labels))
    labels_dict = {}
    for label in labels["labels"]:
        labels_dict[label["name"]] = label["id"]
    # print("labels_dict: {}".format(labels_dict))
    return labels_dict

def old_main():
    """
    Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    service = get_service()

    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])

def get_message_ids_by_query(query_string):
    """
    Returns a list of message ids that match a given query string.
    """
    service = get_service()
    message_results = service.users().messages().list(userId='me', q=query_string).execute()
    # print("message_results: {}".format(message_results))
    if(message_results['resultSizeEstimate'] == 0):
        return []
    return message_results['messages'] if message_results['messages'] is not None else []

def get_message(message_id):
    """
    Returns a dictionary representation of a message from the Gmail API.
    """
    service = get_service()
    message = service.users().messages().get(userId='me', id=message_id).execute()
    return message

def decode_message_part(message_part):
    """
    Returns a string representation of a decoded email message part.
    """
    return base64.urlsafe_b64decode(message_part['body']['data']).decode().strip()

def trim_headers(all_headers, relevant_headers=["From", "To", "Subject", "Date"]):
    """
    Returns a trimmed dictionary representation of an emails headers.
    """
    data = {}
    # print("all headers: {}".format(headers))
    for header in all_headers:
        if header['name'] in relevant_headers:
            data[header['name']] = header['value']

    return data

if __name__ == '__main__':
    # labels_dict = get_labels_dict()
    message_ids = get_message_ids_by_query('from:"chase" subject:"Your Single Transaction Alert from Chase" label:"INBOX" label:"UNREAD"')
    example_message = get_message(message_ids[0]['id'])
    # print("example_message: {}".format(example_message))
    # print("decoded message: {}".format(decode_message_part(example_message['payload'])))
    relevant_headers = trim_headers(example_message['payload']['headers'])
    print("relevant headers: {}".format(relevant_headers))