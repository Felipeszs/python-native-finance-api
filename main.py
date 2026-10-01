from app.controllers.transaction_controller import TransactionController
from app.repositories.transaction_repository import TransactionRepository
from app.routes.router import Router
from app.server import run_server
from app.services.transaction_service import TransactionService

repository = TransactionRepository()

service = TransactionService(repository)

controller = TransactionController(service)

router = Router()

router.add_route(
    "GET",
    "/transactions",
    controller.list_all,
)

router.add_route(
    "POST",
    "/transactions",
    controller.create,
)

router.add_route(
    "GET",
    "/transactions/{id}",
    controller.get_by_id,
)

router.add_route(
    "DELETE",
    "/transactions/{id}",
    controller.delete_by_id,
)

router.add_route(
  "PUT",
  "/transactions/{id}",
  controller.update_by_id,
)

run_server(router)
