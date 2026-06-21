from src.task import Task
from src.course import Course
from src.planner import StudyPlanner


def test_planner_courses_count():
    planner = StudyPlanner()
    course = Course("Python")

    planner.add_course(course)

    assert planner.get_courses_count() == 1