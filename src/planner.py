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

    def get_total_tasks(self):
        total = 0

        for course in self.courses:
            total += len(course.tasks)

        return total

    def get_completed_tasks(self):
        count = 0

        for course in self.courses:
            for task in course.tasks:
                if task.is_completed:
                    count += 1

        return count

    def get_pending_tasks(self):
        return self.get_total_tasks() - self.get_completed_tasks()

    def get_total_estimated_time(self):
        total_time = 0

        for course in self.courses:
            for task in course.tasks:
                total_time += task.estimated_minutes

        return total_time