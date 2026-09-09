import unittest
from decimal import Decimal

from app.models.transaction import Transaction
from app.repositories.transaction_repository import TransactionRepository


class TestTransactionRepository(unittest.TestCase):
    def setUp(self):
        self.repository = TransactionRepository()
        self.transaction = Transaction(
            transaction_type="income",
            value=Decimal("100.00"),
            description="Salary",
        )
        self.repository.save(self.transaction)

    def test_delete_existing_transaction(self):
        deleted = self.repository.delete_by_id(self.transaction.id)

        self.assertTrue(deleted)
        self.assertEqual(self.repository.find_all(), [])

    def test_return_false_when_deleting_unknown_transaction(self):
        deleted = self.repository.delete_by_id(999)

        self.assertFalse(deleted)
        self.assertEqual(self.repository.find_all(), [self.transaction])

    def test_do_not_reuse_deleted_transaction_id(self):
        self.repository.delete_by_id(self.transaction.id)
        next_transaction = Transaction(
            transaction_type="expense",
            value=Decimal("25.00"),
            description="Dinner",
        )

        saved_transaction = self.repository.save(next_transaction)

        self.assertEqual(saved_transaction.id, 2)


if __name__ == "__main__":
    unittest.main()
