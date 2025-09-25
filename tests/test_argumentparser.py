import unittest

from todo.argumentparser import ArgumentParser


class ArgumentParserTest(unittest.TestCase):
    def test_command(self):
        parser = ArgumentParser([])
        self.assertEqual("list", parser.command())
        self.assertEqual("", parser.content())
        parser = ArgumentParser(["add", "toto", "est", "a", "la", "plage"])
        self.assertEqual("add", parser.command())
        self.assertEqual("toto est a la plage", parser.content())
        parser = ArgumentParser(["add"])
        self.assertEqual("add", parser.command())
        self.assertEqual("", parser.content())

    def test_content_as_number(self):
        parser = ArgumentParser(["del", "2"])
        self.assertEqual(2, parser.contentAsNumber())


if __name__ == "__main__":
    unittest.main()
