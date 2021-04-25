from chase_transactions import extract_condensed_message, extract_vendor
from gmail_service import get_service
from gmail_messages import decode_message_part, get_message_ids_by_query, get_message, trim_headers
from gmail_labels import get_labels_dict
import unittest

class LabelTests(unittest.TestCase):

    service = None
    labels_dict = None

    @classmethod
    def setUpClass(cls):
        cls.service = get_service()
        cls.labels_dict = get_labels_dict(cls.service)

    @classmethod
    def tearDownClass(cls):
        cls.service.close()

    def test_get_labels_dict_existing_keys(self):
        labels_dict_keys = self.labels_dict.keys()
        self.assertIn("INBOX", labels_dict_keys)
        self.assertIn("UNREAD", labels_dict_keys)
        self.assertIn("Auto-Finances/Recorded", labels_dict_keys)
        self.assertIn("Auto-Finances/Transaction/Chase", labels_dict_keys)
        self.assertIn("Auto-Finances/Transaction/Discover", labels_dict_keys)

    def test_get_labels_dict_ids(self):
        labels_dict = self.labels_dict
        self.assertEqual(labels_dict["INBOX"], "INBOX")
        self.assertEqual(labels_dict["UNREAD"], "UNREAD")
        self.assertEqual(labels_dict["Auto-Finances/Recorded"], "Label_2163748349047499113")
        self.assertEqual(labels_dict["Auto-Finances/Transaction/Chase"], "Label_1523983363858223337")
        self.assertEqual(labels_dict["Auto-Finances/Transaction/Discover"], "Label_1253373410021274321")

class GetMessageIdTests(unittest.TestCase):

    # for testing purposes I sent an email to paul@paulmatthews.dev from paul@paulmatthews.dev with subject:"Test Subject" body:"test body" label:"Auto-Finances/Transaction/Discover" label:"Auto-Finances/Recorded" label:"Auto-Finances/Transaction/Chase" label:"testing"

    service = None

    def setUp(self):
        self.service = get_service()

    def tearDown(self):
        self.service.close()

    def test_get_message_id_by_query_from(self):
        query_string = 'from:"paul@paulmatthews.dev"'
        message_ids = get_message_ids_by_query(query_string, self.service)
        self.assertGreater(len(message_ids), 0)
        self.assertIn("id", message_ids[0])
        self.assertIn("threadId", message_ids[0])

    def test_get_message_id_by_query_label_recorded(self):
        query_string = 'from:"paul@paulmatthews.dev" label:"Auto-Finances/Recorded'
        message_ids = get_message_ids_by_query(query_string, self.service)
        self.assertGreater(len(message_ids), 0)
        self.assertIn("id", message_ids[0])
        self.assertIn("threadId", message_ids[0])

    def test_get_message_id_by_query_label_chase(self):
        query_string = 'from:"paul@paulmatthews.dev" label:"Auto-Finances/Transaction/Chase'
        message_ids = get_message_ids_by_query(query_string, self.service)
        self.assertGreater(len(message_ids), 0)
        self.assertIn("id", message_ids[0])
        self.assertIn("threadId", message_ids[0])

    def test_get_message_id_by_query_label_discover(self):
        query_string = 'from:"paul@paulmatthews.dev" label:"Auto-Finances/Transaction/Discover'
        message_ids = get_message_ids_by_query(query_string, self.service)
        self.assertGreater(len(message_ids), 0)
        self.assertIn("id", message_ids[0])
        self.assertIn("threadId", message_ids[0])

    def test_get_message_id_by_query_subject(self):
        query_string = 'from:"paul@paulmatthews.dev" subject:"Test Subject"'
        message_ids = get_message_ids_by_query(query_string, self.service)
        self.assertGreater(len(message_ids), 0)
        self.assertIn("id", message_ids[0])
        self.assertIn("threadId", message_ids[0])

class GetMessageTests(unittest.TestCase):

    service = None
    query_string = None
    test_message_id = None
    test_message = None
    labels_dict = None

    @classmethod
    def setUpClass(cls):
        cls.service = get_service()
        cls.query_string = 'from:"paul@paulmatthews.dev" subject:"Test Subject"'
        cls.test_message_id = get_message_ids_by_query(cls.query_string, cls.service)[0]['id']
        cls.test_message = get_message(cls.test_message_id, cls.service)
        cls.labels_dict = get_labels_dict(cls.service)

    @classmethod
    def tearDownClass(cls):
        cls.service.close()

    def test_get_message_results_keys(self):
        self.assertIn("id", self.test_message.keys())
        self.assertIn("threadId", self.test_message.keys())
        self.assertIn("labelIds", self.test_message.keys())
        self.assertIn("snippet", self.test_message.keys())
        self.assertIn("payload", self.test_message.keys())
        self.assertIn("sizeEstimate", self.test_message.keys())
        self.assertIn("historyId", self.test_message.keys())
        self.assertIn("internalDate", self.test_message.keys())
        self.assertGreater(self.test_message['sizeEstimate'], 0)
        
    def test_get_message_results_payload(self):
        payload = self.test_message['payload']
        self.assertIn("partId", payload.keys())
        self.assertIn("headers", payload.keys())
        self.assertIn("body", payload.keys())
        self.assertIn("parts", payload.keys())

    def test_get_message_results_payload_parts(self):
        parts = self.test_message['payload']['parts']
        self.assertGreater(len(parts), 0)
        self.assertIn("partId", parts[0].keys())
        self.assertIn("mimeType", parts[0].keys())
        self.assertIn("headers", parts[0].keys())
        self.assertIn("body", parts[0].keys())
        self.assertIn("size", parts[0]['body'])
        self.assertGreater(parts[0]['body']['size'], 0)
        self.assertIn("data", parts[0]['body'])
        self.assertIsNotNone(parts[0]['body']['data'])

        self.assertIn("partId", parts[1].keys())
        self.assertIn("mimeType", parts[1].keys())
        self.assertIn("headers", parts[1].keys())
        self.assertIn("body", parts[1].keys())
        self.assertIn("size", parts[1]['body'])
        self.assertGreater(parts[1]['body']['size'], 0)
        self.assertIn("data", parts[1]['body'])
        self.assertIsNotNone(parts[1]['body']['data'])

    def test_get_message_results_labels(self):
        message_label_ids = self.test_message['labelIds']
        self.assertIn(self.labels_dict["testing"], message_label_ids)
        self.assertIn(self.labels_dict["Auto-Finances/Recorded"], message_label_ids)
        self.assertIn(self.labels_dict["Auto-Finances/Transaction/Chase"], message_label_ids)
        self.assertIn(self.labels_dict["Auto-Finances/Transaction/Discover"], message_label_ids)

    def test_get_message_check_headers(self):
        headers_keys = [header_dict["name"] for header_dict in self.test_message['payload']['headers']]
        self.assertIn("To", headers_keys)
        self.assertIn("From", headers_keys)
        self.assertIn("Subject", headers_keys)
        self.assertIn("Date", headers_keys)
        self.assertIn("MIME-Version", headers_keys)
        self.assertIn("Message-ID", headers_keys)
        self.assertIn("Content-Type", headers_keys)
    
    def test_trim_headers(self):
        test_trim_headers = trim_headers(self.test_message['payload']['headers'])
        header_keys = test_trim_headers.keys()
        self.assertIn("To", header_keys)
        self.assertIn("From", header_keys)
        self.assertIn("Subject", header_keys)
        self.assertIn("Date", header_keys)
        self.assertEqual("paul@paulmatthews.dev", test_trim_headers["To"])
        self.assertEqual("Paul Matthews <paul@paulmatthews.dev>", test_trim_headers["From"])
        self.assertEqual("Test Subject", test_trim_headers["Subject"])
        # trim_headers should remove the following headers:
        self.assertNotIn("MIME-Version", header_keys)
        self.assertNotIn("Message-ID", header_keys)
        self.assertNotIn("Content-Type", header_keys)
        

    def test_decode_message_part_zero(self):
        part = self.test_message['payload']['parts'][0]
        decoded_message = decode_message_part(part)
        self.assertEqual(decoded_message, "test body")

    def test_decode_message_part_one(self):
        part = self.test_message['payload']['parts'][1]
        decoded_message = decode_message_part(part)
        self.assertEqual(decoded_message, '<div dir="ltr">test body<br></div>')

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

if __name__ == "__main__":
    unittest.main()