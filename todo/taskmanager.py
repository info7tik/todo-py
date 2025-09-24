from colorama import Fore, Style
from pathlib import Path
import json, re
from todo.task import Task, EMPTY_PROJECT

EMPTY_TASKS_LIST = []
NO_INPROGRESS_TASK = -1
IN_PROGRESS_COLOR = Fore.BLUE
TASKS_HEADER = "##### TASKS #####"
DONE_HEADER = "##### DONE #####"


class TaskManager:
    def __init__(self, file_path: str) -> None:
        self.file = file_path
        self.inprogress = NO_INPROGRESS_TASK
        self.todo: list[Task] = list(EMPTY_TASKS_LIST)
        self.done: list[Task] = list(EMPTY_TASKS_LIST)
        self.__next_id = 0
        self.__printed_all_tasks = ""

    def info(self) -> None:
        print(f"configuration file: {self.file}")

    def add(self, task_description: str) -> None:
        assert len(task_description) > 0, "no task description"
        task = self.__create_new_task(task_description)
        self.todo.append(task)
        self.__save()

    def set_task_project(self, task_id: int, new_project: str) -> None:
        assert task_id > 0, "task id must be greater than 0"
        self.__get_todo_task(task_id).project = new_project
        self.__save()

    def __get_todo_task(self, task_id: int) -> Task:
        return self.todo[task_id - 1]

    def build_todo_tasks_str(self) -> str:
        self.__printed_all_tasks = TASKS_HEADER + "\n"
        self.__build_task_list_str(self.todo)
        return self.__printed_all_tasks

    def build_done_tasks_str(self):
        self.__printed_all_tasks = DONE_HEADER + "\n"
        self.__build_task_list_str(self.done)
        return self.__remove_task_indexes()

    def __remove_task_indexes(self):
        task_list_no_index = re.sub(" \\([0-9]{1,3}\\)", '', self.__printed_all_tasks)
        return task_list_no_index

    def __build_task_list_str(self, task_list: list[Task]) -> None:
        if len(task_list) == 0:
            self.__printed_all_tasks += "no tasks"
        else:
            with_project_tasks = self.__sort_tasks_by_project(task_list)
            no_project_tasks = with_project_tasks.pop(EMPTY_PROJECT)
            self.__concat_tasks_with_project(with_project_tasks)
            self.__concat_tasks_no_project(no_project_tasks)
            if self.__printed_all_tasks[-1] == "\n":
                self.__printed_all_tasks = self.__printed_all_tasks[:-1]

    def __sort_tasks_by_project(self, task_list: list[Task]) -> dict[str, list[Task]]:
        sorted_tasks = {"": []}
        for task in task_list:
            if task.project not in sorted_tasks:
                sorted_tasks[task.project] = []
            sorted_tasks[task.project].append(task)
        return sorted_tasks

    def __concat_tasks_with_project(self, tasks: dict[str, list[Task]]) -> None:
        for project in sorted(tasks):
            self.__concat__tasks_str(sorted(tasks[project], key=lambda task: task.description))

    def __concat_tasks_no_project(self, no_project_tasks):
        if len(no_project_tasks) > 0:
            self.__concat__tasks_str(no_project_tasks)

    def __concat__tasks_str(self, tasks: list[Task]) -> None:
        task_descriptions = []
        inprogress_task = [task for task in tasks if task.id == self.inprogress]
        if len(inprogress_task) > 0:
            task_descriptions.append(IN_PROGRESS_COLOR + inprogress_task[0].get_full_description() + Style.RESET_ALL)
        for task in tasks:
            if task.id != self.inprogress:
                task_descriptions.append(task.get_full_description())
        self.__printed_all_tasks += "\n".join(task_descriptions) + "\n"

    def select_inprogress_task(self, task_id: int) -> None:
        assert task_id < len(self.todo) + 1, f"task with id {task_id} does not exist"
        self.inprogress = task_id
        self.__save()

    def delete(self, task_id: int) -> None:
        assert task_id > 0, "task id must be greater than 0"
        assert task_id < len(self.todo) + 1, f"task with id {task_id} does not exist"
        if self.inprogress == task_id:
            self.inprogress = NO_INPROGRESS_TASK
        if self.inprogress != NO_INPROGRESS_TASK and task_id < self.inprogress:
            self.inprogress -= 1
            assert self.inprogress > 0, "task id must be greater than 0, first task has id 1"
        self.__pop_todo_task(task_id)
        self.__save()

    def mark_done(self, task_id: int) -> None:
        assert task_id > 0, "task id must be greater than 0"
        assert task_id < len(self.todo) + 1, f"task with id {task_id} does not exist"
        if self.inprogress == task_id:
            self.inprogress = NO_INPROGRESS_TASK
        if self.inprogress != NO_INPROGRESS_TASK and task_id < self.inprogress:
            self.inprogress -= 1
            assert self.inprogress > 0, "task id must be greater than 0, first task has id 1"
        task = self.__pop_todo_task(task_id)
        self.done.append(task)
        self.__save()

    def __pop_todo_task(self, task_id):
        return self.todo.pop(task_id - 1)

    def delete_done(self):
        self.done = []
        self.__save()

    def load(self) -> None:
        path = Path(self.file)
        if path.is_file():
            self.__load_file()
        else:
            assert not path.is_dir(), f"{self.file} must be a file not a directory"
            directory = path.parents[0]
            assert directory.is_dir(), f"directory {directory} does not exist"
            self.__save()

    def __load_file(self):
        with open(self.file, "r") as json_file:
            configuration = json.load(json_file)
            self.__next_id = 1
            self.todo = self.__load_tasks(configuration["tasks"])
            self.done = self.__load_tasks(configuration["done"])
            self.inprogress = configuration["inprogress"]

    def __load_tasks(self, task_descriptions) -> list:
        new_tasks = []
        for description in task_descriptions:
            try:
                task = self.__create_new_task(description)
                new_tasks.append(task)
                self.__next_id += 1
            except Exception as e:
                print(e)
                print(f"task creation error from '{description}'")
        return new_tasks

    def __create_new_task(self, task_description) -> Task:
        new_task = Task(self.__next_id)
        new_task.load(task_description)
        return new_task

    def __save(self):
        with open(self.file, "w") as json_file:
            configuration = {
                "tasks": [task.build_to_save_str() for task in self.todo],
                "done": [task.build_to_save_str() for task in self.done],
                "inprogress": self.inprogress,
            }
            json.dump(configuration, json_file, indent=4)
