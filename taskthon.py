import os
from argparse import ArgumentParser


def args_parser():

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
    add_parser = subparsers.add_parser('add', help='Add a new task.')
    add_parser.add_argument(
        'description',
        type=str,
        help='Description of the new task.'
    )

    # Update command
    update_parser = subparsers.add_parser('update', help='Update an existing task.')
    update_parser.add_argument(
        'id',
        type=int,
        help='The ID of the task to update.'
    )

    update_parser.add_argument(
        'new_description',
        type=str,
        help='The new description for the task.'
    )

    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete task.')
    delete_parser.add_argument(
        'id',
        type=int,
        help='The ID of the task to delete.'
    )

    list_parser = subparsers.add_parser('list', help='List all tasks.')

    # Status update to 'In Progress'
    mark_in_progress = subparsers.add_parser('mark-in-progress', help='Change status to "In Progress"')
    mark_in_progress.add_argument(
        'id',
        type=int,
        help='The ID of the task to update status'
    )

    # Status update to 'Done'
    mark_in_done = subparsers.add_parser('mark-in-done', help='Change status to "Done"')
    mark_in_done.add_argument(
        'id',
        type=int,
        help='The ID of the task to update status'
    )

    args = parser.parse_args()

    return args