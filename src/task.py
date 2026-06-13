class Task:
    def __init__(self, title, subject, estimated_minutes, priority, deadline):
        self.title = title
        self.subject = subject
        self.estimated_minutes = estimated_minutes
        self.priority = priority
        self.deadline = deadline
        self.is_completed = False

    def mark_completed(self):
        self.is_completed = True

    def mark_uncompleted(self):
        self.is_completed = False

    def __str__(self):
        status = "completed" if self.is_completed else "not completed"

        return (
            f"{self.title} | "
            f"Subject: {self.subject} | "
            f"Time: {self.estimated_minutes} min | "
            f"Priority: {self.priority} | "
            f"Deadline: {self.deadline} | "
            f"Status: {status}"
        )