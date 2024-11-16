#!/bin/python3

import sys, traceback
from todo.taskmanager import TaskManager
from todo.argumentparser import ArgUmentParser

TODO_FILE = "/home/remy/.config/todolist/todo.json"


def main():
    manager = TaskManager(TODO_FILE)
    argumentParser = ArgUmentParser(sys.argv[1:])
    manager.load()
    match argumentParser.command():
        case "add":
            manager.add(argumentParser.content())
        case "clean":
            manager.delete_done()
        case "del":
            manager.delete(argumentParser.contentAsNumber())
        case "info":
            manager.info()
        case "done":
            manager.mark_done(argumentParser.contentAsNumber())
        case "list":
            print(manager.build_todo_tasks_str())
            print(manager.build_done_tasks_str())
        case "project":
            manager.set_task_project(*argumentParser.contentAsStringAndNumber())
        case "take":
            task_id = argumentParser.content()
            if task_id.isdigit():
                manager.select_inprogress_task(int(task_id))
            else:
                print("take option requires a valid task id. Example: take <number>")
        case _:
            print("command not found: " + argumentParser.command())


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
