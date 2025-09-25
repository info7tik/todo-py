#!/bin/python3

import sys
import traceback
from os import getenv

from todo.argumentparser import ArgumentParser
from todo.pathbuilder import PathBuilder
from todo.taskmanager import TaskManager

CONFIGURATION_FILE = "todo.json"


def main():
    builder = PathBuilder()
    file_path = builder.build(getenv("HOME", ""), CONFIGURATION_FILE)
    manager = TaskManager(file_path)
    argumentParser = ArgumentParser(sys.argv[1:])
    manager.load_configuration()
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
