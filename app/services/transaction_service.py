from app.models.transaction import Transaction

class TransactionService:

  def __init__(self, repository):
    self.repository = repository

  def create_transaction(
        self,
        transaction_type,
        value,
        description
    ):
    transaction = Transaction(
            transaction_type=transaction_type,
            value=value,
            description=description
        )
    return self.repository.save(transaction)

  def list_transactions(self):
        return self.repository.find_all()
