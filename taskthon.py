import os
from argparse import ArgumentParser


def main():

    parser = ArgumentParser(
        description="Taskthon is a CLI todo tool to manage your todo tasks from the convenient of your terminal.",
    )
    parser.add_argument("--db", help="Path to the database file (default: '~/taskthon.json'", default="~/taskthon.json")

    subparsers = parser.add_subparsers(
        dest='command',
        required=True,
        help="Available commands: add, update, delete, list"
    )

    # Add command