'''
test message 2

---------- Forwarded message ---------
From: Chase <no.reply.alerts@chase.com>
Date: Fri, Apr 23, 2021 at 6:50 PM
Subject: Your Single Transaction Alert from Chase
To: <paul@paulmatthews.dev>



This is an Alert to help you manage your credit card account ending in 8824.

As you requested, we are notifying you of any charges over the amount of
($USD) 0.00, as specified in your Alert settings.
A charge of ($USD) 51.28 at WALGREENS #9436 has been authorized on Apr 23,
2021 at 7:50 PM ET.

Do not reply to this Alert.

If you have questions, please call the number on the back of your credit
card, or send a secure message from your Inbox on www.chase.com.

To see all of the Alerts available to you, or to manage your Alert
settings, please log on to www.chase.com.
'''

'''
test message 1

---------- Forwarded message ---------
From: Chase <no.reply.alerts@chase.com>
Date: Fri, Apr 23, 2021 at 11:58 AM
Subject: Your Single Transaction Alert from Chase
To: <paul@paulmatthews.dev>



This is an Alert to help you manage your credit card account ending in 8824.

As you requested, we are notifying you of any charges over the amount of
($USD) 0.00, as specified in your Alert settings.
A charge of ($USD) 12.47 at CHICK-FIL-A #03077 has been authorized on Apr
23, 2021 at 12:58 PM ET.

Do not reply to this Alert.

If you have questions, please call the number on the back of your credit
card, or send a secure message from your Inbox on www.chase.com.

To see all of the Alerts available to you, or to manage your Alert
settings, please log on to www.chase.com.
'''

from gmail_messages import decode_message_part, trim_headers
import re

def extract_condensed_message(string_full_message):
    condensed_message_parts = string_full_message.split(", as specified in your Alert settings.\r\n")
    extracted_condensed_message = condensed_message_parts[1].split('.\r\n')[0]
    return extracted_condensed_message.replace("\r\n", " ")

def extract_vendor(condensed_message):
    vendor = condensed_message.split(" at ")[1].split(" has ")[0]
    return vendor
    
def extract_amount(condensed_message):
    return float(re.search('\d+[.]\d+', condensed_message).group().strip())

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
    full_message = decode_message_part(message['payload']['parts'][0])
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