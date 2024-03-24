import unittest

from todo.task import Task, EMPTY_PROJECT, EMPTY_DESCRIPTION


class TaskTest(unittest.TestCase):
    def test_load_task(self):
        task = Task(1)
        self.assertEqual(1, task.id)
        self.assertEqual(EMPTY_PROJECT, task.project)
        self.assertEqual(EMPTY_DESCRIPTION, task.description)
        project1 = "project 1"
        description1 = "super project"
        task.load(f"{project1}: {description1}")
        self.assertEqual(project1, task.project)
        self.assertEqual(description1, task.description)
        project2 = "project 2"
        description2 = "super project with : for retrieving full description"
        task.load(f" {project2} : {description2} ")
        self.assertEqual(project2, task.project)
        self.assertEqual(description2, task.description)
        task.load(description1)
        self.assertEqual(EMPTY_PROJECT, task.project)
        self.assertEqual(description1, task.description)

    def test_full_description(self):
        project = "project 1"
        description = "project description"
        task_id = 1
        task = Task(task_id)
        task.project = ""
        task.description = description
        self.assertEqual(description + f" ({task_id})", task.get_full_description())
        task.project = project
        self.assertEqual(f"[{project}] {description} ({task_id})", task.get_full_description())


if __name__ == "__main__":
    unittest.main()
