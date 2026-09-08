from decimal import Decimal, InvalidOperation


class TransactionController:
    def __init__(self, service):
        self.service = service

    def create(self, body):
        transaction_type = body["transaction_type"]
        description = body["description"]

        try:
            value = Decimal(body["value"])
        except (InvalidOperation, TypeError):
            raise ValueError("value must be a valid decimal") from None

        return self.service.create_transaction(
            transaction_type,
            value,
            description,
        )

    def list_all(self):
        return self.service.list_transactions()
