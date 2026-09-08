from decimal import Decimal


class Transaction:
    def __init__(
        self,
        transaction_type: str,
        value: Decimal,
        description: str
    ):
        if not isinstance(description, str):
            raise TypeError("description must be a string")

        if not description.strip():
            raise ValueError("description cannot be empty")

        if not isinstance(value, Decimal):
            raise TypeError("value must be a Decimal")

        if value <= 0:
            raise ValueError("value must be greater than zero")

        if transaction_type not in ("income", "expense"):
            raise ValueError(
                "transaction_type must be 'income' or 'expense'"
            )

        self.id = None
        self.transaction_type = transaction_type
        self.value = value
        self.description = description.strip()
