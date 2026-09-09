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
