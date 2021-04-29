import unittest
from gmail.service import get_service
from gmail.messages import decode_message_part, get_message, get_message_ids_by_query
from transactions.discover import extract_condensed_message, extract_vendor, extract_amount, extract_authorized_time, discover_message_to_dict

'''
test email:
Transaction threshold exceeded

You've set an account alert to let you know if a purchase or cash advance exceeds your specified amount. This alert is just informational: we've processed the transaction as usual.

Transaction Date: April 18, 2021
Merchant: 5GUYS 1048 ECOMM
Amount: $36.09

If you don't recognize this transaction, call us at 1-800-DISCOVER (1-800-347-2683).
'''

class DiscoverTransactionsTests(unittest.TestCase):

    service = None
    test_query_string = 'from:"discover@service.discover.com" subject:"Transaction Alert" label:"testing"'
    test_message_id = None
    test_message = None
    condensed_message = None

    @classmethod
    def setUpClass(cls):
        cls.service = get_service()
        cls.test_message_id = get_message_ids_by_query(cls.test_query_string, cls.service)[0]['id']
        cls.test_message = get_message(cls.test_message_id, cls.service)
        cls.condensed_message = extract_condensed_message(decode_message_part(cls.test_message['payload']['parts'][0]))

    def testExtractCondensedMessage(self):
        expected = "Transaction Date:: April 18, 2021;Merchant: 5GUYS 1048 ECOMM;Amount: $36.09"
        actual = self.condensed_message
        self.assertEqual(expected, actual)

    def testExtractVendor(self):
        expected_vendor = "5GUYS 1048 ECOMM"
        actual_vendor = extract_vendor(self.condensed_message)
        self.assertEqual(expected_vendor, actual_vendor)

    def testExtractAmount(self):
        expected_amount = "36.09"
        actual_amount = extract_amount(self.condensed_message)
        self.assertEqual(expected_amount, actual_amount)

    def testExtractAuthorizedTime(self):
        expected_time = "April 18, 2021"
        actual_time = extract_authorized_time(self.condensed_message)
        self.assertEqual(expected_time, actual_time)

    def testDiscoverMessageToDict(self):
        self.maxDiff = None
        expected_dict = {
            "To": "paul.matthews1989@gmail.com",
            "From": "Discover Card <discover@service.discover.com>",
            "Date": "18 Apr 2021 13:56:26 -0400",
            "Subject": "Transaction Alert",
            "authorized_time": "April 18, 2021",
            "vendor": "5GUYS 1048 ECOMM",
            "amount": "36.09",
            "gmail_message_id": "178e6206f0d8f12b",
            "gmail_thread_id": "178e6206f0d8f12b",
            "account": "discover_credit",
            "condensed_message": "Transaction Date:: April 18, 2021;Merchant: 5GUYS 1048 ECOMM;Amount: $36.09"
        }
        actual_dict = discover_message_to_dict(self.test_message)
        self.assertDictEqual(expected_dict, actual_dict)