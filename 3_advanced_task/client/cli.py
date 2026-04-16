#!/usr/bin/env python3

import argparse

from commands.menu_commands import handle_list_menu


def build_parser():
    parser = argparse.ArgumentParser(description="Pizza ordering CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("menu", help="List pizza menu")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "menu":
        handle_list_menu()


if __name__ == "__main__":
    main()