import base64

def get_message_ids_by_query(query_string, service):
    """
    Returns a list of message ids that match a given query string.
    """
    message_results = service.users().messages().list(userId='me', q=query_string).execute()
    if(message_results['resultSizeEstimate'] == 0):
        return []
    return message_results['messages'] if message_results['messages'] is not None else []

def get_message(message_id, service):
    """
    Returns a dictionary representation of a message from the Gmail API.
    """
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
    for header in all_headers:
        if header['name'] in relevant_headers:
            data[header['name']] = header['value']

    return data