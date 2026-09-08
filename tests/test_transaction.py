import unittest
from decimal import Decimal

from app.models.transaction import Transaction


class TestTransaction(unittest.TestCase):
    def test_create_valid_income_transaction(self):
        transaction = Transaction(
            transaction_type="income",
            value=Decimal("100.00"),
            description="Salary",
        )

        self.assertIsNone(transaction.id)
        self.assertEqual(transaction.transaction_type, "income")
        self.assertEqual(transaction.value, Decimal("100.00"))
        self.assertEqual(transaction.description, "Salary")

    def test_create_valid_expense_transaction(self):
        transaction = Transaction(
            transaction_type="expense",
            value=Decimal("49.90"),
            description="Groceries",
        )

        self.assertEqual(transaction.transaction_type, "expense")

    def test_strip_description_whitespace(self):
        transaction = Transaction(
            transaction_type="income",
            value=Decimal("100.00"),
            description="  Salary  ",
        )

        self.assertEqual(transaction.description, "Salary")

    def test_reject_description_that_is_not_a_string(self):
        for invalid_description in (None, 100, Decimal("10.00")):
            with self.subTest(description=invalid_description):
                with self.assertRaisesRegex(
                    TypeError,
                    "description must be a string",
                ):
                    Transaction(
                        transaction_type="income",
                        value=Decimal("100.00"),
                        description=invalid_description,
                    )

    def test_reject_empty_description(self):
        for invalid_description in ("", "   "):
            with self.subTest(description=invalid_description):
                with self.assertRaisesRegex(
                    ValueError,
                    "description cannot be empty",
                ):
                    Transaction(
                        transaction_type="income",
                        value=Decimal("100.00"),
                        description=invalid_description,
                    )

    def test_reject_value_that_is_not_a_decimal(self):
        for invalid_value in (None, 100, 100.0, "100.00"):
            with self.subTest(value=invalid_value):
                with self.assertRaisesRegex(
                    TypeError,
                    "value must be a Decimal",
                ):
                    Transaction(
                        transaction_type="income",
                        value=invalid_value,
                        description="Salary",
                    )

    def test_reject_value_that_is_not_greater_than_zero(self):
        for invalid_value in (Decimal("0"), Decimal("-0.01")):
            with self.subTest(value=invalid_value):
                with self.assertRaisesRegex(
                    ValueError,
                    "value must be greater than zero",
                ):
                    Transaction(
                        transaction_type="income",
                        value=invalid_value,
                        description="Salary",
                    )

    def test_reject_invalid_transaction_type(self):
        for invalid_type in (None, "", "transfer", "INCOME"):
            with self.subTest(transaction_type=invalid_type):
                with self.assertRaisesRegex(
                    ValueError,
                    "transaction_type must be 'income' or 'expense'",
                ):
                    Transaction(
                        transaction_type=invalid_type,
                        value=Decimal("100.00"),
                        description="Salary",
                    )


if __name__ == "__main__":
    unittest.main()
