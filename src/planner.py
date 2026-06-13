class StudyPlanner:
    def __init__(self):
        self.courses = []

    def add_course(self, course):
        self.courses.append(course)

    def remove_course(self, course):
        if course in self.courses:
            self.courses.remove(course)

    def get_courses_count(self):
        return len(self.courses)