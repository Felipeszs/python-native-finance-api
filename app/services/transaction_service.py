from app.models.transaction import Transaction


class TransactionService:
    def __init__(self, repository):
        self.repository = repository

    def create_transaction(
        self,
        transaction_type,
        value,
        description,
    ):
        transaction = Transaction(
            transaction_type=transaction_type,
            value=value,
            description=description,
        )
        return self.repository.save(transaction)

    def list_transactions(self):
        return self.repository.find_all()

    def get_transaction_by_id(self, transaction_id):
        transaction = self.repository.find_by_id(transaction_id)

        if transaction is None:
            raise LookupError("transaction not found")

        return transaction

    def delete_transaction_by_id(self, transaction_id):
        deleted = self.repository.delete_by_id(transaction_id)

        if not deleted:
            raise LookupError("transaction not found")
