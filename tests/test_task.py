from src.task import Task


def test_task_creation():
    task = Task(
        "Homework",
        "Python",
        60,
        1,
        "2026-06-20"
    )

    assert task.title == "Homework"
    assert task.subject == "Python"
    assert task.estimated_minutes == 60
    assert task.is_completed == False