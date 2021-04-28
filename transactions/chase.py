import re
from gmail.messages import decode_message_part, trim_headers

def extract_condensed_message(string_full_message):
    condensed_message_parts = string_full_message.split(", as specified in your Alert settings.\r\n")
    extracted_condensed_message = condensed_message_parts[1].split('.\r\n')[0]
    return extracted_condensed_message.replace("\r\n", " ")

def extract_vendor(condensed_message):
    vendor = condensed_message.split(" at ")[1].split(" has ")[0]
    return vendor
    
def extract_amount(condensed_message):
    return re.search('\d+[.]\d+', condensed_message).group().strip()

def extract_authorized_time(condensed_message):
    return condensed_message.split("has been authorized on ")[1]

def chase_message_to_dict(message):
    chase_dict = {}

    # grab gmail message id & thread id
    chase_dict["gmail_message_id"] = message['id']
    chase_dict["gmail_thread_id"] = message['threadId']

    # grab relevant headers ["From", "To", "Subject", "Date"]
    
    for rhk, rhv in trim_headers(message['payload']['headers']).items():
        chase_dict[rhk] = rhv

    # grab and decode the full message from the message payload

    # TODO: test for the case of a message not having multiple parts and therefore the body that needs to be decoded is message['payload'] instead of message['payload']['parts'][0] -> this seems to be when the gmail API returns a response with multiple representations of the email, one in plaintext and another in HTML. We may be able to check the headers for the data format and predict if it will have parts or not.
    full_message = None
    if 'parts' in message['payload'].keys():
        full_message = decode_message_part(message['payload']['parts'][0])
    else:
        full_message = decode_message_part(message['payload'])
    # chase_dict["full_message"] = decode_message_part(message['payload']['parts'][0])

    # extract condensed message from full message
    chase_dict["condensed_message"] = extract_condensed_message(full_message)
    # print("condensed_message: {}".format(chase_dict["condensed_message"]))

    # extract vendor fromm condensed_message
    chase_dict["vendor"] = extract_vendor(chase_dict["condensed_message"])

    # extract amount from condensed_message
    chase_dict["amount"] = extract_amount(chase_dict["condensed_message"])

    # extract authorized_time from condensed_message
    chase_dict["authorized_time"] = extract_authorized_time(chase_dict["condensed_message"])

    # add chase_credit as the account
    chase_dict["account"] = "chase_credit"

    return chase_dict