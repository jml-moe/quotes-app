from .methods import do_something
from huey.contrib.djhuey import task

@task()
def task_do_something():
    do_something()
    return "Task completed!"