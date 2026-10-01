class TransactionRepository:
    def __init__(self):
        self.transactions = []
        self.next_id = 1

    def save(self, transaction):
        transaction.id = self.next_id
        self.next_id += 1

        self.transactions.append(transaction)

        return transaction

    def find_all(self):
        return self.transactions

    def find_by_id(self, transaction_id):
        for transaction in self.transactions:
            if transaction.id == transaction_id:
                return transaction
        return None

    def delete_by_id(self, transaction_id):
        transaction = self.find_by_id(transaction_id)

        if transaction is None:
            return False

        self.transactions.remove(transaction)
        return True

    def update_by_id(self, transaction_id, update_transaction):
        for index, transaction in enumerate(self.transactions):
            if transaction.id == transaction_id:
                update_transaction.id = transaction.id
                self.transactions[index] = update_transaction
                return update_transaction

        return None
