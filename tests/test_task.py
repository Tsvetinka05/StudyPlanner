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

def test_mark_completed():
    task = Task(
        "Homework",
        "Python",
        60,
        1,
        "2026-06-20"
    )

    task.mark_completed()

    assert task.is_completed == True