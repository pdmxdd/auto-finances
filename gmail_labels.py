def get_labels_dict(service):
    """
    Returns a dictionary of Gmail labels key: name value: id.
    """
    labels = service.users().labels().list(userId="me").execute()
    labels_dict = {}
    for label in labels["labels"]:
        labels_dict[label["name"]] = label["id"]
    return labels_dict