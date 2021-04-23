from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_credentials():
    """
    Returns the credentials in token.json. If it doesn't exist, or is not valid it will intiate the OAuth 2.0 flow to get a new token.json using the local credentials.json.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

def get_service():
    """
    Returns the Gmail API service of the user. the service is the entrypoint to interfacing with the Gmail API.
    """
    service = build('gmail', 'v1', credentials=get_credentials())

    return service

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
    print("message_results: {}".format(message_results))
    if(message_results['resultSizeEstimate'] == 0):
        return []
    return message_results['messages'] if message_results['messages'] is not None else []

if __name__ == '__main__':
    # labels_dict = get_labels_dict()
    message_ids = get_message_ids_by_query('from:"chase" subject:"Your Single Transaction Alert from Chase" label:"INBOX" label:"UNREAD"')
    print("message_ids: {}".format(message_ids))