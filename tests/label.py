from gmail_labels import get_labels_dict
from gmail_service import get_service
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