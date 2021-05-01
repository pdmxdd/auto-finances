import unittest
from tests.label import LabelTests
from tests.message_id import GetMessageIdTests
from tests.message import GetMessageTests
from tests.transactions_chase import ChaseTransactionsTests
from tests.write_transactions import WriteTransactionTests
from tests.message_labels import MessageRemoveLabelTests
from tests.transactions_discover import DiscoverTransactionsTests
from tests.aws import AWSTests

if __name__ == "__main__":
    unittest.main()