from app.controllers.transaction_controller import TransactionController
from app.controllers.category_controller import CategoryController

from app.repositories.transaction_repository import TransactionRepository
from app.repositories.category_repository import CategoryRepository

from app.services.transaction_service import TransactionService
from app.services.category_service import CategoryService

from app.views.transaction_view import TransactionView
from app.views.category_view import CategoryView

from app.routes.router import Router
from app.server import run_server


# TRANSACTION
transaction_repository = TransactionRepository()
category_repository = CategoryRepository()
transaction_service = TransactionService(transaction_repository, category_repository)
transaction_controller = TransactionController(transaction_service)


# CATEGORY
category_service = CategoryService(category_repository)
category_controller = CategoryController(category_service)


# ROUTER
router = Router()


# TRANSACTION ROUTES

router.add_route(
    "GET",
    "/transactions",
    transaction_controller.list_all,
    TransactionView.serialize_transactions
)

router.add_route(
    "POST",
    "/transactions",
    transaction_controller.create,
    TransactionView.serialize_transaction
)

router.add_route(
    "GET",
    "/transactions/{id}",
    transaction_controller.get_by_id,
    TransactionView.serialize_transaction
)

router.add_route(
    "DELETE",
    "/transactions/{id}",
    transaction_controller.delete_by_id,
    TransactionView.serialize_transaction
)

router.add_route(
    "PUT",
    "/transactions/{id}",
    transaction_controller.update_by_id,
    TransactionView.serialize_transaction
)


# CATEGORY ROUTES

router.add_route(
    "GET",
    "/categories",
    category_controller.list_all,
    CategoryView.serialize_categories
)

router.add_route(
    "POST",
    "/categories",
    category_controller.create,
    CategoryView.serialize_category
)

router.add_route(
    "GET",
    "/categories/{id}",
    category_controller.get_by_id,
    CategoryView.serialize_category
)


# SERVER
if __name__ == "__main__":
    run_server(router)
