from app.repositories.transaction_repository import TransactionRepository
from app.services.transaction_service import TransactionService
from app.controllers.transaction_controller import TransactionController
from app.routes.router import Router
from app.server import run_server


repository = TransactionRepository()

service = TransactionService(repository)

controller = TransactionController(service)

router = Router()

router.add_route(
    "GET",
    "/transactions",
    controller.list_all
)

router.add_route(
    "POST",
    "/transactions",
    controller.create
)

router.add_route(
    "GET",
    "/transactions/{id}",
    controller.get_by_id
)

run_server(router)
