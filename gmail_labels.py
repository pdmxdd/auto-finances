from gmail_service import get_service

def get_labels_dict(service):
    """
    Returns a dictionary of Gmail labels key: name value: id.
    """
    # service = get_service()
    labels = service.users().labels().list(userId="me").execute()
    # print("labels: {}".format(labels))
    labels_dict = {}
    for label in labels["labels"]:
        labels_dict[label["name"]] = label["id"]
    # print("labels_dict: {}".format(labels_dict))
    return labels_dict