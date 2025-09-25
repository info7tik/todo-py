import unittest

from tests.test_argumentparser import ArgumentParserTest
from tests.test_pathbuilder import PathBuilderTest
from tests.test_task import TaskTest
from tests.test_taskmanager import TaskManagerTest


if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(ArgumentParserTest))
    suite.addTest(loader.loadTestsFromTestCase(PathBuilderTest))
    suite.addTest(loader.loadTestsFromTestCase(TaskTest))
    suite.addTest(loader.loadTestsFromTestCase(TaskManagerTest))
    runner = unittest.TextTestRunner()
    runner.run(suite)
