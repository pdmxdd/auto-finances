import unittest
from gmail.service import get_service
from gmail.labels import get_labels_dict
from gmail.messages import get_message_ids_by_query, get_message, remove_labels_from_message, add_labels_to_message

class MessageRemoveLabelTests(unittest.TestCase):

    service = None
    labels_dict = None
    query_string = 'from:"paul@paulmatthews.dev" subject:"Test Subject"'
    test_message = None

    @classmethod
    def setUpClass(cls):
        cls.service = get_service()
        cls.labels_dict = get_labels_dict(cls.service)
        cls.test_message = get_message(get_message_ids_by_query(cls.query_string, cls.service)[0]['id'], cls.service)

    @classmethod
    def tearDownClass(cls):
        cls.service.close()

    def setUp(self):
        if self.labels_dict["testing"] not in self.test_message["labelIds"]:
            add_labels_to_message(self.test_message['id'], [self.labels_dict["testing"]], self.service)
        if self.labels_dict["Auto-Finances/Recorded"] not in self.test_message["labelIds"]:
            add_labels_to_message(self.test_message['id'], [self.labels_dict["Auto-Finances/Recorded"]], self.service)
        if self.labels_dict["Auto-Finances/Transaction/Chase"] not in self.test_message["labelIds"]:
            add_labels_to_message(self.test_message['id'], [self.labels_dict["Auto-Finances/Transaction/Chase"]], self.service)
        if self.labels_dict["Auto-Finances/Transaction/Discover"] not in self.test_message["labelIds"]:
            add_labels_to_message(self.test_message['id'], [self.labels_dict["Auto-Finances/Transaction/Discover"]], self.service)

        self.test_message = get_message(self.test_message['id'], self.service)

    def tearDown(self):
        if self.labels_dict["testing"] not in self.test_message["labelIds"]:
            add_labels_to_message(self.test_message['id'], [self.labels_dict["testing"]], self.service)
        if self.labels_dict["Auto-Finances/Recorded"] not in self.test_message["labelIds"]:
            add_labels_to_message(self.test_message['id'], [self.labels_dict["Auto-Finances/Recorded"]], self.service)
        if self.labels_dict["Auto-Finances/Transaction/Chase"] not in self.test_message["labelIds"]:
            add_labels_to_message(self.test_message['id'], [self.labels_dict["Auto-Finances/Transaction/Chase"]], self.service)
        if self.labels_dict["Auto-Finances/Transaction/Discover"] not in self.test_message["labelIds"]:
            add_labels_to_message(self.test_message['id'], [self.labels_dict["Auto-Finances/Transaction/Discover"]], self.service)

        self.test_message = get_message(self.test_message['id'], self.service)

    def test_setup_desired_state(self):
        self.assertIn(self.labels_dict["testing"], self.test_message["labelIds"])
        self.assertIn(self.labels_dict["Auto-Finances/Recorded"], self.test_message["labelIds"])
        self.assertIn(self.labels_dict["Auto-Finances/Transaction/Chase"], self.test_message["labelIds"])
        self.assertIn(self.labels_dict["Auto-Finances/Transaction/Discover"], self.test_message["labelIds"])

    def test_remove_and_add_labels(self):
        remove_label_ids = [
            self.labels_dict["Auto-Finances/Transaction/Chase"],
            self.labels_dict["Auto-Finances/Transaction/Discover"]
        ]

        remove_labels_from_message(self.test_message["id"], remove_label_ids, self.service)

        self.test_message = get_message(self.test_message['id'], self.service)

        self.assertIn(self.labels_dict["testing"], self.test_message["labelIds"])
        self.assertIn(self.labels_dict["Auto-Finances/Recorded"], self.test_message["labelIds"])
        self.assertNotIn(self.labels_dict["Auto-Finances/Transaction/Chase"], self.test_message["labelIds"])
        self.assertNotIn(self.labels_dict["Auto-Finances/Transaction/Discover"], self.test_message["labelIds"])

        add_labels_to_message(self.test_message["id"], remove_label_ids, self.service)

        self.test_message = get_message(self.test_message["id"], self.service)

        self.assertIn(self.labels_dict["testing"], self.test_message["labelIds"])
        self.assertIn(self.labels_dict["Auto-Finances/Recorded"], self.test_message["labelIds"])
        self.assertIn(self.labels_dict["Auto-Finances/Transaction/Chase"], self.test_message["labelIds"])
        self.assertIn(self.labels_dict["Auto-Finances/Transaction/Discover"], self.test_message["labelIds"])

        

    