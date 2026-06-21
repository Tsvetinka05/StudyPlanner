from src.task import Task
from src.course import Course
from src.planner import StudyPlanner
from src.database import Database

planner = StudyPlanner()

python_course = Course("Python")

task1 = Task(
    "Finish homework",
    "Python",
    90,
    1,
    "2026-06-20"
)

task2 = Task(
    "Study OOP",
    "Python",
    120,
    2,
    "2026-06-25"
)

database = Database()
database.create_tables()

database.add_task(task1)
database.add_task(task2)

task1.mark_completed()

python_course.add_task(task1)
python_course.add_task(task2)

planner.add_course(python_course)

print("Courses:", planner.get_courses_count())
print("Total tasks:", planner.get_total_tasks())
print("Completed tasks:", planner.get_completed_tasks())
print("Pending tasks:", planner.get_pending_tasks())
print("Total study time:", planner.get_total_estimated_time(), "minutes")
print("Tasks saved to database.")
