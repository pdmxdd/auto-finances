from gmail.messages import decode_message_part, trim_headers


def extract_condensed_message(string_full_message):
    # discover was giving me more issues than Chase with their gratuitous use of returns and carriage returns. so i converted it to a raw string, this allowed me to more plainly see how I should split the string
    raw_string = string_full_message.encode('unicode-escape').decode()
    chopped_message = raw_string.split("usual.\\r\\n\\r\\n")[1].split("\\r\\n\\r\\n\\r\\nIf")[0]
    condensed_message = chopped_message.replace("\\r\\n\\r\\n", ";")
    return condensed_message

def extract_vendor(condensed_message):
    return condensed_message.split(";")[1][10:]

def extract_amount(condensed_message):
    return condensed_message.split(";")[2][9:]

def extract_authorized_time(condensed_message):
    return condensed_message.split(";")[0][19:]

def discover_message_to_dict(message):
    discover_dict = {}

    discover_dict["gmail_message_id"] = message['id']
    discover_dict["gmail_thread_id"] = message['threadId']

    for rhk, rhv in trim_headers(message['payload']['headers']).items():
        discover_dict[rhk] = rhv

    full_message = None
    if 'parts' in message['payload'].keys():
        full_message = decode_message_part(message['payload']['parts'][0])
    else:
        full_message = decode_message_part(message['payload'])

    discover_dict["condensed_message"] = extract_condensed_message(full_message)

    discover_dict["vendor"] = extract_vendor(discover_dict["condensed_message"])

    discover_dict["amount"] = extract_amount(discover_dict["condensed_message"])

    discover_dict["authorized_time"] = extract_authorized_time(discover_dict["condensed_message"])

    discover_dict["account"] = "discover_credit"

    return discover_dict