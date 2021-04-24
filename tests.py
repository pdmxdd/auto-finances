from gmail_service import get_service
from gmail_messages import get_message_ids_by_query
from gmail_labels import get_labels_dict
import unittest

class LabelTests(unittest.TestCase):

    service = None

    def setUp(self):
        self.service = get_service()

    def tearDown(self):
        self.service.close()

    def test_get_labels_dict_existing_keys(self):
        labels_dict_keys = get_labels_dict(self.service).keys()
        self.assertIn("INBOX", labels_dict_keys)
        self.assertIn("UNREAD", labels_dict_keys)
        self.assertIn("Auto-Finances/Recorded", labels_dict_keys)
        self.assertIn("Auto-Finances/Transaction/Chase", labels_dict_keys)
        self.assertIn("Auto-Finances/Transaction/Discover", labels_dict_keys)

    def test_get_labels_dict_ids(self):
        labels_dict = get_labels_dict(self.service)
        self.assertEqual(labels_dict["INBOX"], "INBOX")
        self.assertEqual(labels_dict["UNREAD"], "UNREAD")
        self.assertEqual(labels_dict["Auto-Finances/Recorded"], "Label_2163748349047499113")
        self.assertEqual(labels_dict["Auto-Finances/Transaction/Chase"], "Label_1523983363858223337")
        self.assertEqual(labels_dict["Auto-Finances/Transaction/Discover"], "Label_1253373410021274321")

class MessageTests(unittest.TestCase):

    # for testing purposes I sent an email to paul@paulmatthews.dev from paul@paulmatthews.dev with subject:"Test Subject" body:"test body" label:"Auto-Finances/Transaction/Discover" label:"Auto-Finances/Recorded" label:"Auto-Finances/Transaction/Chase" label:"testing"

    # after refactoring lables to take a service instead of creating a new one in function it cut down the number of "ResourceWarnings" around SSLSockets from 6 to 2. defintely on the right path
    service = None

    def setUp(self):
        self.service = get_service()

    def tearDown(self):
        self.service.close()

    def test_get_message_id_by_query_from(self):
        query_string = 'from:"paul@paulmatthews.dev"'
        message_ids = get_message_ids_by_query(query_string)
        self.assertGreater(len(message_ids), 0)
        self.assertIn("id", message_ids[0])
        self.assertIn("threadId", message_ids[0])

    def test_get_message_id_by_query_label_recorded(self):
        query_string = 'from:"paul@paulmatthews.dev" label:"Auto-Finances/Recorded'
        message_ids = get_message_ids_by_query(query_string)
        self.assertGreater(len(message_ids), 0)
        self.assertIn("id", message_ids[0])
        self.assertIn("threadId", message_ids[0])

    def test_get_message_id_by_query_label_chase(self):
        query_string = 'from:"paul@paulmatthews.dev" label:"Auto-Finances/Transaction/Chase'
        message_ids = get_message_ids_by_query(query_string)
        self.assertGreater(len(message_ids), 0)
        self.assertIn("id", message_ids[0])
        self.assertIn("threadId", message_ids[0])

    def test_get_message_id_by_query_label_discover(self):
        query_string = 'from:"paul@paulmatthews.dev" label:"Auto-Finances/Transaction/Discover'
        message_ids = get_message_ids_by_query(query_string)
        self.assertGreater(len(message_ids), 0)
        self.assertIn("id", message_ids[0])
        self.assertIn("threadId", message_ids[0])

    def test_get_message_id_by_query_subject(self):
        query_string = 'from:"paul@paulmatthews.dev" subject:"Test Subject"'
        message_ids = get_message_ids_by_query(query_string)
        self.assertGreater(len(message_ids), 0)
        self.assertIn("id", message_ids[0])
        self.assertIn("threadId", message_ids[0])

    # FIX: when running tests I am getting the following error: "...../home/paul/personal/coding/auto-finances/env_auto_finances/lib/python3.8/site-packages/six.py:589: ResourceWarning: unclosed <ssl.SSLSocket fd=3, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=6, laddr=('192.168.1.9', 52650), raddr=('172.217.4.202', 443)> return iter(d.items(**kw))"

    # pretty straight forward an SSLSocket is not being closed, probably do to the nature that for every single test I have a new service being created and it's not gracefully closing before the next test creates a new service. I need to refactor so that my tests only use one service per class is what I'm thinking

    # TODO: get_message tests, decode_message_part tests, trim_headers tests


if __name__ == "__main__":
    unittest.main()