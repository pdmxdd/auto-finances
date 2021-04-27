import unittest
from gmail_service import get_service
from gmail_messages import get_message_ids_by_query, get_message, decode_message_part
from chase_transactions import extract_amount, extract_authorized_time, extract_condensed_message, extract_vendor, chase_message_to_dict

class ChaseTransactionsTests(unittest.TestCase):

    service = None
    test_message_1 = None
    test_message_2 = None
    @classmethod
    def setUpClass(cls):
        cls.service = get_service()
        test_message_ids = get_message_ids_by_query('from:"paul@paulmatthews.dev" subject:"Your Single Transaction Alert From Chase"', cls.service)
        cls.test_message_1 = get_message(test_message_ids[0]['id'], cls.service)
        cls.test_message_2 = get_message(test_message_ids[1]['id'], cls.service)
        cls.service.close()

    def setUp(self):
        self.service = get_service()

    def tearDown(self):
        self.service.close()

    def testExtractCondensedMessage(self):
        condensed_message_1 = extract_condensed_message(decode_message_part(self.test_message_1['payload']['parts'][0]))
        self.assertEqual('A charge of ($USD) ', condensed_message_1[0:19])
        self.assertEqual('A charge of ($USD) 51.28 at WALGREENS #9436 has been authorized on Apr 23, 2021 at 7:50 PM ET', condensed_message_1)

        condensed_message_2 = extract_condensed_message(decode_message_part(self.test_message_2['payload']['parts'][0]))
        self.assertEqual('A charge of ($USD) ', condensed_message_2[0:19])
        self.assertEqual('A charge of ($USD) 12.47 at CHICK-FIL-A #03077 has been authorized on Apr 23, 2021 at 12:58 PM ET', condensed_message_2)

    def testExtractVendor(self):
        condensed_message_1 = extract_condensed_message(decode_message_part(self.test_message_1['payload']['parts'][0]))
        self.assertEqual("WALGREENS #9436", extract_vendor(condensed_message_1))

        condensed_message_2 = extract_condensed_message(decode_message_part(self.test_message_2['payload']['parts'][0]))
        self.assertEqual("CHICK-FIL-A #03077", extract_vendor(condensed_message_2))

    def testExtractAmount(self):
        condensed_message_1 = extract_condensed_message(decode_message_part(self.test_message_1['payload']['parts'][0]))
        self.assertEqual("51.28", extract_amount(condensed_message_1))

        condensed_message_2 = extract_condensed_message(decode_message_part(self.test_message_2['payload']['parts'][0]))
        self.assertEqual("12.47", extract_amount(condensed_message_2))

    def testExtractAuthorizedTime(self):
        condensed_message_1 = extract_condensed_message(decode_message_part(self.test_message_1['payload']['parts'][0]))
        self.assertEqual("Apr 23, 2021 at 7:50 PM ET", extract_authorized_time(condensed_message_1))

        condensed_message_2 = extract_condensed_message(decode_message_part(self.test_message_2['payload']['parts'][0]))
        self.assertEqual("Apr 23, 2021 at 12:58 PM ET", extract_authorized_time(condensed_message_2))

    def testChaseMessageToDict(self):
        self.maxDiff = None
        expected_dict_1 = {
            "To": "paul@paulmatthews.dev",
            "From": "Paul Matthews <paul@paulmatthews.dev>",
            "Date": "Sat, 24 Apr 2021 23:39:21 -0500",
            "Subject": "Fwd: Your Single Transaction Alert from Chase",
            "authorized_time": "Apr 23, 2021 at 7:50 PM ET",
            "vendor": "WALGREENS #9436",
            "amount": "51.28",
            "gmail_message_id": "17907532dd229b2a",
            "gmail_thread_id": "178ffab904b01c52",
            "account": "chase_credit",
            "condensed_message": "A charge of ($USD) 51.28 at WALGREENS #9436 has been authorized on Apr 23, 2021 at 7:50 PM ET",
        }
        self.assertDictEqual(expected_dict_1, chase_message_to_dict(self.test_message_1))

        expected_dict_2 = {
            "To": "paul@paulmatthews.dev",
            "From": "Paul Matthews <paul@paulmatthews.dev>",
            "Date": "Sat, 24 Apr 2021 23:39:05 -0500",
            "Subject": "Fwd: Your Single Transaction Alert from Chase",
            "authorized_time": "Apr 23, 2021 at 12:58 PM ET",
            "vendor": "CHICK-FIL-A #03077",
            "amount": "12.47",
            "gmail_message_id": "1790752ef8865f12",
            "gmail_thread_id": "178ffab904b01c52",
            "account": "chase_credit",
            "condensed_message": "A charge of ($USD) 12.47 at CHICK-FIL-A #03077 has been authorized on Apr 23, 2021 at 12:58 PM ET",
        }      
        self.assertDictEqual(expected_dict_2, chase_message_to_dict(self.test_message_2))  