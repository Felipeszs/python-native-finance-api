class TransactionView:

  @staticmethod
  def serialize_transaction(transaction):
    return {
      "id" : transaction.id,
      "type" : transaction.transaction_type,
      "value" : transaction.value,
      "description" : transaction.description
    }

  @staticmethod
  def serialize_transactions(transactions):
    return [
      TransactionView.serialize_transaction(transaction)
      for transaction in transactions
    ]

