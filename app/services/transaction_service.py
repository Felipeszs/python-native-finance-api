from app.models.transaction import Transaction


class TransactionService:
    def __init__(self, transaction_repository, category_repository):
        self.transaction_repository = transaction_repository
        self.category_repository = category_repository

    def create_transaction(
        self,
        transaction_type,
        value,
        description,
        category_id,
    ):
        category = self.category_repository.find_by_id(category_id)
        if category is None:
            raise LookupError("category not found")

        transaction = Transaction(
            transaction_type=transaction_type,
            value=value,
            description=description,
            category_id=category_id,
        )
        return self.transaction_repository.save(transaction)

    def list_transactions(self):
        return self.transaction_repository.find_all()

    def get_transaction_by_id(self, transaction_id):
        transaction = self.transaction_repository.find_by_id(transaction_id)

        if transaction is None:
              raise LookupError("transaction not found")

        return transaction

    def delete_transaction_by_id(self, transaction_id):
        deleted = self.transaction_repository.delete_by_id(transaction_id)

        if not deleted:
              raise LookupError("transaction not found")

    def update_transaction_by_id(
        self, transaction_id, transaction_type, value, description, category_id
    ):

        if self.category_repository.find_by_id(category_id) is None:
            raise LookupError("category not found")

        update_transaction = Transaction(
            transaction_type=transaction_type,
            value=value,
            description=description,
            category_id=category_id,
        )

        transaction = self.transaction_repository.update_by_id(transaction_id, update_transaction)

        if transaction is None:
              raise LookupError("transaction not found")

        return transaction
