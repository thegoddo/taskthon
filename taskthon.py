from argparse import ArgumentParser
import json
from tabulate import tabulate
from datetime import datetime
from pathlib import Path


def main():
    args = args_parser()
    db_path = Path(args.db).expanduser()
    tasks = load_tasks(db_path)

    match args.command:
        case 'add':
            new_id = len(tasks) + 1
            current_time = get_timestamp()

            new_task = {
                'id': new_id,
                'description': args.description,
                'status': 'pending',
                'createAt': current_time,
                'updateAt': current_time
            }

            tasks.append(new_task)
            save_tasks(db_path, tasks)
            print(f'Task added with ID: {new_id}')

        case 'update':
            current_time = get_timestamp()
            for task in tasks:
                if task['id'] == args.id:
                    task['description'] = args.new_description
                    task['updateAt'] = current_time
                    save_tasks(db_path, tasks)
                    print(f'Tasks {args.id} updated')
                    break
                else:
                    print(f'Error: Task ID {args.id} not found.')
        case 'delete':
            task_id_to_delete = args.id

            initial_length = len(tasks)

            tasks = [task for task in tasks if task['id'] != task_id_to_delete]

            if len(tasks) < initial_length:
                save_tasks(db_path, tasks)
                print(f'Task with ID {task_id_to_delete} is deleted successfully.')
            else:
                print(f'Error: Task ID {task_id_to_delete} is not found.')
        case 'list':
            display_list(args.d_type, tasks)
        case 'status':
            current_time = get_timestamp()
            task_id_to_change = args.id
            for task in tasks:
                if task[id] == task_id_to_change:
                    task['status'] = args.new_status
                    task['updateAt'] = current_time
                    save_tasks(db_path, tasks)
                    print(f'Task with ID {task_id_to_change} status updated successfully.')
                    break
                else:
                    print(f'Error: Task ID {task_id_to_change} is not found.')
        case _:
            print(f'Error: Something went Wrong!!!')



def display_list(d_type: str, tasks: list):

    if not tasks:
        print("No task found!!!")
        return

    headers = ["ID", "Status", "Description", "Create At", "Update At"]
    table_date = []
    new_tasks = [task for task in tasks if task['status'] != d_type]

    for task in new_tasks:
        create_at_short = task.get("createAt", "").replace("T", "")
        update_at_short = task.get("updateAt", "").replace("T", "")

        table_date.append([
            task.get("id"),
            task.get("status").capitalize(),
            task.get("description"),
            create_at_short,
            update_at_short
        ])

        print(tabulate(table_date, headers, tablefmt="fancy_grid"))



def get_timestamp() -> str:
    return datetime.now().isoformat()


def save_tasks(db_path: Path, tasks: list):
    # Make sure the directory exists
    db_path.parent.mkdir(parents=True, exist_ok=True)

    with open(db_path, 'w') as f:
        json.dump(tasks, f, indent=4)


def load_tasks(db_path: Path) -> list:
    if not db_path.exists() or db_path.stat().st_size == 0:
        return []

    try:
        with open(db_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f'Error: Database file at {db_path} contains invalid JSON.')
        return []


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
    list_parser.add_argument(
        'd_type',
        choices=['all', 'done', 'in-progress', 'pending'],
        help="The type of task you want to list."
    )

    mark = subparsers.add_parser('status', help='Update status.')
    mark.add_argument(
        'id',
        type=int,
        help='The ID to update todo status.'
    )

    mark.add_argument(
        'new_status',
        choices=['pending', 'in-progress', 'done'],
        help="The new status (e.g., pending, in-progress, done)."
    )

    args = parser.parse_args()

    return args


if __name__ == '__main__':
    main()
