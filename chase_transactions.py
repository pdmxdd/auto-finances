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

def extract_condensed_message(string_full_message):
    condensed_message_parts = string_full_message.split(", as specified in your Alert settings.\r\n")
    extracted_condensed_message = condensed_message_parts[1].split('.\r\n')[0]
    return extracted_condensed_message.replace("\r\n", " ")

def extract_vendor(condensed_message):
    vendor = condensed_message.split(" at ")[1].split(" has ")[0]
    return vendor
    