import unittest
from pathlib import Path

from colorama import Style

from todo.task import Task
from todo.taskmanager import DONE_HEADER, IN_PROGRESS_COLOR, NO_INPROGRESS_TASK, TASKS_HEADER, TaskManager

NON_EMPTY_CONFIGURATION_FILE = "tests/resources/config.json"
TEMPORARY_CONFIGURATION_FILE = "tests/resources/temp.json"


class TaskManagerTest(unittest.TestCase):
    def test_load_conf(self):
        json_path = NON_EMPTY_CONFIGURATION_FILE
        manager = TaskManager(json_path)
        manager.load_configuration()
        self.assertEqual(123456789, manager.inprogress)
        self.assertEqual(4, len(manager.todo))
        self.assertEqual(3, len(manager.done))

    def test_load_not_existing_file(self):
        json_path = "tests/resources/not_existing_file"
        self.__delete_file(json_path)
        manager = TaskManager(json_path)
        self.assertEqual(NO_INPROGRESS_TASK, manager.inprogress)
        self.assertEqual(0, len(manager.todo))
        self.assertEqual(0, len(manager.done))
        manager.load_configuration()
        self.assertEqual(NO_INPROGRESS_TASK, manager.inprogress)
        self.assertEqual(0, len(manager.todo))
        self.assertEqual(0, len(manager.done))
        path = Path(json_path)
        self.assertTrue(path.is_file())
        self.__delete_file(json_path)

    def test_load_not_existing_directory(self):
        manager = TaskManager("not_existing_dir/not_existing_file")
        manager.load_configuration()
        config_file = Path(manager.file)
        self.assertTrue(config_file.is_file())

    def test_add_task(self):
        manager = self.__create_temporary_manager()
        self.assertEqual(0, len(manager.todo))
        description = "one more task"
        manager.add(description)
        self.assertEqual(1, len(manager.todo))
        self.assertEqual(description, manager.todo[0].description)
        project = "one project"
        description = "one more task"
        manager.add(f"{project}: {description}")
        self.assertEqual(2, len(manager.todo))
        self.assertEqual(description, manager.todo[1].description)
        self.assertEqual(project, manager.todo[1].project)
        self.__delete_temporary_configuration()

    def test_add_task_then_reload(self):
        manager = self.__create_temporary_manager()
        self.assertEqual(0, len(manager.todo))
        project = "one project"
        description = "one more task"
        manager.add(f"{project}: {description}")
        self.assertEqual(1, len(manager.todo))
        self.assertEqual(description, manager.todo[0].description)
        self.assertEqual(project, manager.todo[0].project)
        manager.load_configuration()
        self.assertEqual(1, len(manager.todo))
        self.assertEqual(description, manager.todo[0].description)
        self.assertEqual(project, manager.todo[0].project)
        self.__delete_temporary_configuration()

    def test_list_tasks(self):
        manager = TaskManager(NON_EMPTY_CONFIGURATION_FILE)
        manager.load_configuration()
        todo_tasks = manager.build_todo_tasks_str()
        self.assertEqual(
            TASKS_HEADER + "\n[Project 1] Task 1 (2)\n[Project 4] Task 4 (3)\n[Project 4] Task 6 (1)\nTask 7 (4)",
            todo_tasks,
        )
        done_tasks = manager.build_done_tasks_str()
        self.assertEqual(DONE_HEADER + "\n[Project 2] Task 2\n[Project 2] Task 5\n[Project 3] Task 3", done_tasks)

    def test_list_empty_configuration(self):
        manager = self.__create_temporary_manager()
        todo_tasks = manager.build_todo_tasks_str()
        self.assertEqual(TASKS_HEADER + "\nno tasks", todo_tasks)
        done_tasks = manager.build_done_tasks_str()
        self.assertEqual(DONE_HEADER + "\nno tasks", done_tasks)
        self.__delete_temporary_configuration()

    def test_list_tasks_with_inprogress(self):
        manager = self.__create_temporary_manager_with_3_tasks()
        task1_id = self.__get_task_id(manager, "task1")
        self.assertEqual(NO_INPROGRESS_TASK, manager.inprogress)
        manager.select_inprogress_task(task1_id)
        self.assertEqual(task1_id, manager.inprogress)
        self.__delete_temporary_configuration()
        todo_tasks = manager.build_todo_tasks_str()
        self.assertEqual(
            TASKS_HEADER
            + "\n"
            + IN_PROGRESS_COLOR
            + "[project1] task1 (1)"
            + Style.RESET_ALL
            + "\n[project1] task2 (2)\n[project2] task3 (3)",
            todo_tasks,
        )
        self.__delete_temporary_configuration()

    def test_delete_task(self):
        manager = self.__create_temporary_manager_with_3_tasks()
        task2_id = self.__get_task_id(manager, "task2")
        self.assertEqual(3, len(manager.todo))
        self.assertEqual(0, len(manager.done))
        manager.delete(task2_id)
        manager.load_configuration()
        self.assertEqual(2, len(manager.todo))
        self.assertEqual(0, len(manager.done))
        task2 = [task for task in manager.todo if task.description == "task2"]
        self.assertEqual(0, len(task2))
        with self.assertRaises(AssertionError, msg="task ids starts at 1"):
            manager.delete(0)
        self.assertEqual(2, len(manager.todo))

        manager.delete(1)
        self.assertEqual(1, len(manager.todo))
        manager.delete(1)
        self.assertEqual(0, len(manager.todo))
        self.__delete_temporary_configuration()

    def test_delete_task_with_inprogress(self):
        manager = self.__create_temporary_manager_with_3_tasks()
        task2_id = self.__get_task_id(manager, "task2")
        task3_id = self.__get_task_id(manager, "task3")

        manager.select_inprogress_task(task3_id)
        manager.delete(task2_id)
        manager.load_configuration()
        task2 = [task for task in manager.todo if task.description == "task2"]
        self.assertEqual(0, len(task2))
        new_task3_id = self.__get_task_id(manager, "task3")
        self.assertEqual(new_task3_id, manager.inprogress)

        manager.delete(new_task3_id)
        task3 = [task for task in manager.todo if task.description == "task3"]
        self.assertEqual(0, len(task3))
        self.assertEqual(NO_INPROGRESS_TASK, manager.inprogress)
        self.__delete_temporary_configuration()

    def test_mark_done(self):
        manager = self.__create_temporary_manager_with_3_tasks()
        task2_id = self.__get_task_id(manager, "task2")
        self.assertEqual(3, len(manager.todo))
        self.assertEqual(0, len(manager.done))
        manager.mark_done(task2_id)
        self.assertEqual(2, len(manager.todo))
        self.assertEqual(1, len(manager.done))
        with self.assertRaises(AssertionError, msg="task2 does not exist in todo tasks"):
            self.__get_task(manager, "task2")
        self.__delete_temporary_configuration()

    def test_delete_done(self):
        manager = self.__create_temporary_manager_with_3_tasks()
        task2_id = self.__get_task_id(manager, "task2")
        self.assertEqual(0, len(manager.done))
        manager.mark_done(task2_id)
        self.assertEqual(1, len(manager.done))
        manager.delete_done()
        manager.load_configuration()
        self.assertEqual(0, len(manager.done))

    def test_set_task_project(self):
        manager = self.__create_temporary_manager_with_3_tasks()
        manager.add("no project")
        no_project_task = self.__get_task(manager, "no project")
        project_name = "one-project"
        self.assertEqual("", no_project_task.project)
        manager.set_task_project(no_project_task.id, project_name)
        manager.load_configuration()
        no_project_task = self.__get_task(manager, "no project")
        self.assertEqual(project_name, no_project_task.project)
        self.__delete_temporary_configuration()

    def __create_temporary_manager_with_3_tasks(self) -> TaskManager:
        manager = self.__create_temporary_manager()
        manager.add("project1: task1")
        manager.add("project1: task2")
        manager.add("project2: task3")
        manager.load_configuration()
        return manager

    def __get_task(self, manager: TaskManager, task_description) -> Task:
        task = [task for task in manager.todo if task.description == task_description]
        assert len(task) > 0, f"can not find task from {task_description}"
        return task[0]

    def __get_task_id(self, manager: TaskManager, task_description) -> int:
        task_id = [task.id for task in manager.todo if task.description == task_description]
        assert len(task_id) > 0, f"can not find task from {task_description}"
        return task_id[0]

    def __create_temporary_manager(self) -> TaskManager:
        self.__delete_file(TEMPORARY_CONFIGURATION_FILE)
        return TaskManager(TEMPORARY_CONFIGURATION_FILE)

    def __delete_temporary_configuration(self) -> None:
        self.__delete_file(TEMPORARY_CONFIGURATION_FILE)

    def __delete_file(self, json_path: str):
        path = Path(json_path)
        if path.is_file():
            path.unlink()
        self.assertFalse(path.is_file())


if __name__ == "__main__":
    unittest.main()
