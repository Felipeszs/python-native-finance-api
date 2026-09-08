
class TransactionController:
  def __init__(self, service):
    self.service = service

  def create(self, body):
    transaction_type = body['transaction_type']
    value = body['value']
    description = body['description']

    return self.service.create.create_transaction(transaction_type, value, description)

