from gmail_messages import get_message_ids_by_query
from gmail_labels import get_labels_dict
import unittest

class LabelTests(unittest.TestCase):

    def test_get_labels_dict_existing_keys(self):
        labels_dict_keys = get_labels_dict().keys()
        self.assertIn("INBOX", labels_dict_keys)
        self.assertIn("UNREAD", labels_dict_keys)
        self.assertIn("Auto-Finances/Recorded", labels_dict_keys)
        self.assertIn("Auto-Finances/Transaction/Chase", labels_dict_keys)
        self.assertIn("Auto-Finances/Transaction/Discover", labels_dict_keys)

    def test_get_labels_dict_ids(self):
        labels_dict = get_labels_dict()
        self.assertEqual(labels_dict["INBOX"], "INBOX")
        self.assertEqual(labels_dict["UNREAD"], "UNREAD")
        self.assertEqual(labels_dict["Auto-Finances/Recorded"], "Label_2163748349047499113")
        self.assertEqual(labels_dict["Auto-Finances/Transaction/Chase"], "Label_1523983363858223337")
        self.assertEqual(labels_dict["Auto-Finances/Transaction/Discover"], "Label_1253373410021274321")

class MessageTests(unittest.TestCase):

    # for testing purposes I sent an email to paul@paulmatthews.dev from paul@paulmatthews.dev with subject:"Test Subject" body:"test body" label:"Auto-Finances/Transaction/Discover" label:"Auto-Finances/Recorded" label:"Auto-Finances/Transaction/Chase" label:"testing"

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

    # TODO: get_message tests, decode_message_part tests, trim_headers tests


if __name__ == "__main__":
    unittest.main()