from decimal import Decimal


class TransactionController:
    def __init__(self, service):
        self.service = service

    def create(self, body):
        transaction_type = body["transaction_type"]
        value = Decimal(body["value"])
        description = body["description"]

        return self.service.create_transaction(
            transaction_type,
            value,
            description,
        )

    def list_all(self):
        return self.service.list_transactions()
