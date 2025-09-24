# Python ToDo List
A simple todo list manager with a command line interface.

## Installation
```
sudo ln -s /path/to/main.py /usr/bin/todo (create a link to the executable Python script)
```

## Usage
* List all todo tasks with their identifiers: `todo`
* Add new tasks: `todo add "my task without project"`
* Add new tasks associated to a project: `todo add "my-nice-project: my new task"`
* Edit the project of tasks: `todo project 2` (2 is the identifier of the task)
* Mark tasks done: `todo done 2` (2 is the identifier of the task)
* Remove all done tasks to the todo list: `todo clean`
* Display the path to the configuration file: `todo info`
* Select the current task: `todo take 2`

## Example
```
> todo add "first task"
> todo add "my-project: first task with project"
> todo add "my done task"
> todo done 3
> todo
##### TASKS #####
[my-project] first task with project (2)
first task (1)
##### DONE #####
my done task
```

## Developers
* Installation
```
mkdir env
python3 -m venv env
source env/bin/activate
python3 -m pip install -r requirements.txt
```
* Run the tests
```
python3 test_suite.py
```
* Add tests
* Edit the file [test_suite.py](./test_suite.py) and add the following lines:
```
from tests.mynewtest import MyNewTest
[...]
suite.addTest(loader.loadTestsFromTestCase(MyNewTest))
```
