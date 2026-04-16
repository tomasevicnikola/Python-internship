import argparse
from commands.menu_commands import handle_list_menu
from commands.order_commands import handle_create_order


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

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "menu":
        handle_list_menu()
    elif args.command == "create-order":
        handle_create_order(args.customer_name, args.address, args.item)


if __name__ == "__main__":
    main()