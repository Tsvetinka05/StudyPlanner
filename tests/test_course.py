from src.course import Course
from src.task import Task


def test_add_task():
    course = Course("Python")

    task = Task(
        "Homework",
        "Python",
        60,
        1,
        "2026-06-20"
    )

    course.add_task(task)

    assert course.get_tasks_count() == 1