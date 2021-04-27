import unittest
from gmail_service import get_service
from gmail_messages import get_message_ids_by_query


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