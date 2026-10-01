from decimal import Decimal, InvalidOperation


class InvalidTransactionId(ValueError):
    pass


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

        return self.service.create_transaction(transaction_type, value, description)

    def list_all(self):
        return self.service.list_transactions()

    def get_by_id(self, id):
        try:
            transaction_id = int(id)
        except (ValueError, TypeError):
            raise ValueError("id must be a valid integer") from None

        return self.service.get_transaction_by_id(transaction_id)

    def delete_by_id(self, id):
        try:
            transaction_id = int(id)
        except (ValueError, TypeError):
            raise ValueError("id must be a valid integer") from None

        return self.service.delete_transaction_by_id(transaction_id)

    def update_by_id(self, body, id):
        try:
            transaction_id = int(id)
        except (ValueError, TypeError):
            raise InvalidTransactionId("id must be a valid integer") from None

        transaction_type = body["transaction_type"]
        description = body["description"]

        try:
            value = Decimal(body["value"])
        except (InvalidOperation, TypeError):
            raise ValueError("value must be a valid decimal") from None

        return self.service.update_transaction_by_id(
            transaction_id,
            transaction_type,
            value,
            description,
        )
