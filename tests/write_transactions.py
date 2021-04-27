import unittest, os
from gmail.service import get_service
from gmail_messages import get_message_ids_by_query, get_message
from chase_transactions import chase_message_to_dict
from csv_utils import delete_file, write_dict_list, read_csv

class WriteTransactionTests(unittest.TestCase):

    service = None

    test_message_dict_1 = None
    test_message_dict_2 = None
    test_csv_file = './expenses.test.csv'
    test_query_string = 'from:"paul@paulmatthews.dev" subject:"Your Single Transaction Alert From Chase"'
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
    

    @classmethod
    def setUpClass(cls):
        cls.service = get_service()
        messages = [get_message(message_id['id'], cls.service) for message_id in get_message_ids_by_query(cls.test_query_string, cls.service)]
        cls.test_message_dict_1 = chase_message_to_dict(messages[0])
        cls.test_message_dict_2 = chase_message_to_dict(messages[1])

    @classmethod
    def tearDownClass(cls):
        cls.service.close()

    def tearDown(self):
        delete_file(self.test_csv_file)

    def test_write_dict_list(self):
        self.assertFalse(os.path.exists(self.test_csv_file))

        write_dict_list(self.test_csv_file, [self.test_message_dict_1])
        self.assertTrue(os.path.exists(self.test_csv_file))
        self.assertTrue(os.path.isfile(self.test_csv_file))

    def test_read_csv(self):
        self.assertFalse(os.path.exists(self.test_csv_file))

        write_dict_list(self.test_csv_file, [self.test_message_dict_1])

        data = read_csv(self.test_csv_file)
        self.assertDictEqual(self.expected_dict_1, data[0])

    def test_write_row_to_csv(self):
        self.assertFalse(os.path.exists(self.test_csv_file))

        write_dict_list(self.test_csv_file, [self.test_message_dict_1])

        write_dict_list(self.test_csv_file, [self.expected_dict_2])

        self.maxDiff = None

        data = read_csv(self.test_csv_file)
        self.assertDictEqual(self.expected_dict_2, data[1])
        self.assertDictEqual(self.expected_dict_1, data[0])