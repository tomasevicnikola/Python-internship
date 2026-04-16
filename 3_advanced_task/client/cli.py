import argparse
from commands.admin_commands import (
    handle_add_pizza,
    handle_delete_pizza,
    handle_force_cancel_order,
)
from commands.menu_commands import handle_list_menu
from commands.order_commands import (
    handle_cancel_order,
    handle_create_order,
    handle_get_order,
)


def build_parser():
    parser = argparse.ArgumentParser(description="Pizza ordering CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("menu", help="List pizza menu")

    order_parser = subparsers.add_parser("create-order", help="Create a new order")
    order_parser.add_argument("--customer-name", required=True, help="Customer name")
    order_parser.add_argument("--address", required=True, help="Delivery address")
    order_parser.add_argument(
        "--item",
        action="append",
        required=True,
        help="Order item in format pizza_id:quantity. Can be used multiple times.",
    )

    status_parser = subparsers.add_parser("get-order", help="Get order by ID")
    status_parser.add_argument("--order-id", type=int, required=True, help="Order ID")

    cancel_parser = subparsers.add_parser("cancel-order", help="Cancel order by ID")
    cancel_parser.add_argument("--order-id", type=int, required=True, help="Order ID")

    add_pizza_parser = subparsers.add_parser("add-pizza", help="Add pizza to menu (admin)")
    add_pizza_parser.add_argument("--token", required=True, help="Admin token")
    add_pizza_parser.add_argument("--name", required=True, help="Pizza name")
    add_pizza_parser.add_argument("--price", type=float, required=True, help="Pizza price")
    add_pizza_parser.add_argument(
        "--is-available",
        default="true",
        help="Whether pizza is available: true/false",
    )

    delete_pizza_parser = subparsers.add_parser(
        "delete-pizza",
        help="Delete pizza from menu (admin)",
    )
    delete_pizza_parser.add_argument("--token", required=True, help="Admin token")
    delete_pizza_parser.add_argument("--pizza-id", type=int, required=True, help="Pizza ID")

    force_cancel_parser = subparsers.add_parser(
        "admin-cancel-order",
        help="Force-cancel order (admin)",
    )
    force_cancel_parser.add_argument("--token", required=True, help="Admin token")
    force_cancel_parser.add_argument("--order-id", type=int, required=True, help="Order ID")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "menu":
        handle_list_menu()
    elif args.command == "create-order":
        handle_create_order(args.customer_name, args.address, args.item)
    elif args.command == "get-order":
        handle_get_order(args.order_id)
    elif args.command == "cancel-order":
        handle_cancel_order(args.order_id)
    elif args.command == "add-pizza":
        handle_add_pizza(args.token, args.name, args.price, args.is_available)
    elif args.command == "delete-pizza":
        handle_delete_pizza(args.token, args.pizza_id)
    elif args.command == "admin-cancel-order":
        handle_force_cancel_order(args.token, args.order_id)


if __name__ == "__main__":
    main()