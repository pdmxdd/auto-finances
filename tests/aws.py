import unittest
from unittest.case import expectedFailure
from utils.aws import delete_file_from_bucket, get_bucket, get_object, upload_file_to_bucket

class AWSTests(unittest.TestCase):

    bucket_name = "auto-finances"
    bucket = get_bucket(bucket_name)
    test_file = 'test.test'

    def setUp(self):
        delete_file_from_bucket(self.bucket_name, self.test_file)

    def tearDown(self):
        delete_file_from_bucket(self.bucket_name, self.test_file)

    @unittest.expectedFailure
    def testSetUp(self):
        test_object = get_object(self.bucket_name, self.test_file)
        expectedFailure(test_object.get())

    def test_get_bucket(self):
        self.assertEqual(self.bucket_name, self.bucket.name)
        self.assertIsNotNone(self.bucket.creation_date)

    def test_upload_to_bucket(self):
        upload_file_to_bucket(self.bucket_name, self.test_file)
        test_object = get_object(self.bucket_name, self.test_file)
        self.assertEqual(200, test_object.get()['ResponseMetadata']['HTTPStatusCode'])
        