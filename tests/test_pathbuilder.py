from unittest import TestCase

from todo.pathbuilder import PathBuilder


class PathBuilderTest(TestCase):
    def test_build(self):
        builder = PathBuilder()
        root_dir = "tests/resources"
        filename = "todo.json"
        self.assertEqual(f"{root_dir}/.config/{filename}", builder.build(root_dir, filename))

    def test_build_with_empty_dir(self):
        builder = PathBuilder()
        root_dir = ""
        filename = "todo.json"
        with self.assertRaises(Exception) as context:
            builder.build(root_dir, filename)
        self.assertTrue("empty" in str(context.exception))

    def test_build_not_existing_dir(self):
        builder = PathBuilder()
        root_dir = "tests/not_existing_dir"
        filename = "todo.json"
        with self.assertRaises(Exception) as context:
            builder.build(root_dir, filename)
        self.assertTrue("not exist" in str(context.exception))

    def test_build_with_file_instead_of_dir(self):
        builder = PathBuilder()
        root_dir = "tests/test_pathbuilder.py"
        filename = "todo.json"
        with self.assertRaises(Exception) as context:
            builder.build(root_dir, filename)
        self.assertTrue("is a file" in str(context.exception))
