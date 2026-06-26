import tkinter as tk
import calendar
from tkinter import messagebox
from datetime import datetime

from src.task import Task
from src.database import Database


def start_gui():
    window = tk.Tk()
    window.title("Study Planner")
    window.geometry("600x600")

    tasks = []

    database = Database()
    database.create_tables()

    def clear_placeholder(entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)

    def add_placeholder(entry, placeholder):
        if entry.get() == "":
            entry.insert(0, placeholder)

    def add_task():
        task_text = task_entry.get()
        subject = subject_entry.get()
        time_text = time_entry.get()
        deadline = deadline_entry.get()

        if task_text == "" or task_text == "Task name":
            messagebox.showerror("Task Error", "Please enter a task name.")
            return

        if subject == "" or subject == "Subject":
            messagebox.showerror("Task Error", "Please enter a subject.")
            return

        if time_text == "" or time_text == "Estimated minutes":
            messagebox.showerror("Task Error", "Please enter the estimated study time.")
            return

        if not time_text.isdigit():
            messagebox.showerror("Task Error", "Estimated study time must contain only numbers.")
            return

        estimated_time = int(time_text)

        if estimated_time <= 0:
            messagebox.showerror("Task Error", "Estimated study time must be greater than 0.")
            return

        if deadline == "" or deadline == "Deadline":
            messagebox.showerror("Task Error", "Please enter a deadline.")
            return

        try:
            datetime.strptime(deadline, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Task Error", "Deadline must be in format YYYY-MM-DD.")
            return

        task = Task(
            task_text,
            subject,
            estimated_time,
            1,
            deadline
        )

        database.add_task(task)

        task_display = f"{task_text} | {subject} | {estimated_time} min | {deadline}"

        tasks.append(task_display)
        task_listbox.insert(tk.END, task_display)

        task_entry.delete(0, tk.END)
        subject_entry.delete(0, tk.END)
        time_entry.delete(0, tk.END)
        deadline_entry.delete(0, tk.END)

        add_placeholder(task_entry, "Task name")
        add_placeholder(subject_entry, "Subject")
        add_placeholder(time_entry, "Estimated minutes")
        add_placeholder(deadline_entry, "Deadline")

        messagebox.showinfo("Success", "Task added successfully!")

    def complete_task():
        selected_task = task_listbox.curselection()

        if not selected_task:
            messagebox.showwarning("Warning", "Please select a task.")
            return

        index = selected_task[0]
        task_text = tasks[index]

        if "completed" not in task_text:
            tasks[index] = task_text + " - completed"

        task_listbox.delete(index)
        task_listbox.insert(index, tasks[index])

    def delete_task():
        selected_task = task_listbox.curselection()

        if not selected_task:
            messagebox.showwarning("Warning", "Please select a task.")
            return

        index = selected_task[0]
        task_text = tasks[index]

        task_title = task_text.split("|")[0].strip()

        database.delete_task_by_title(task_title)

        task_listbox.delete(index)
        tasks.pop(index)

    def show_statistics():
        completed = 0

        for task in tasks:
            if "completed" in task:
                completed += 1

        pending = len(tasks) - completed

        messagebox.showinfo(
            "Statistics",
            f"Total tasks: {len(tasks)}\n"
            f"Completed: {completed}\n"
            f"Pending: {pending}"
        )

    title = tk.Label(
        window,
        text="Study Planner",
        font=("Arial", 20)
    )
    title.pack(pady=20)

    task_entry = tk.Entry(window, width=40)
    task_entry.pack(pady=5)
    task_entry.insert(0, "Task name")
    task_entry.bind("<FocusIn>", lambda event: clear_placeholder(task_entry, "Task name"))
    task_entry.bind("<FocusOut>", lambda event: add_placeholder(task_entry, "Task name"))

    subject_entry = tk.Entry(window, width=40)
    subject_entry.pack(pady=5)
    subject_entry.insert(0, "Subject")
    subject_entry.bind("<FocusIn>", lambda event: clear_placeholder(subject_entry, "Subject"))
    subject_entry.bind("<FocusOut>", lambda event: add_placeholder(subject_entry, "Subject"))

    time_entry = tk.Entry(window, width=40)
    time_entry.pack(pady=5)
    time_entry.insert(0, "Estimated minutes")
    time_entry.bind("<FocusIn>", lambda event: clear_placeholder(time_entry, "Estimated minutes"))
    time_entry.bind("<FocusOut>", lambda event: add_placeholder(time_entry, "Estimated minutes"))

    deadline_entry = tk.Entry(window, width=40)
    deadline_entry.pack(pady=5)
    deadline_entry.insert(0, "Deadline")
    deadline_entry.bind("<FocusIn>", lambda event: clear_placeholder(deadline_entry, "Deadline"))
    deadline_entry.bind("<FocusOut>", lambda event: add_placeholder(deadline_entry, "Deadline"))


    def show_break_recommendation():
        total_minutes = 0

        for task in tasks:
            parts = task.split("|")

            if len(parts) >= 3:
                time_part = parts[2].strip()
                minutes = int(time_part.replace("min", "").strip())
                total_minutes += minutes

        if total_minutes == 0:
            messagebox.showinfo("Study Breaks", "No study time available.")
            return

        breaks = total_minutes // 50

        messagebox.showinfo(
            "Study Breaks",
            f"Total study time: {total_minutes} minutes\n"
            f"Recommended breaks: {breaks}\n\n"
            "Recommendation: Take a 10 minute break after every 50 minutes of studying."
        )
    
    def generate_study_plan():
        today = datetime.today()

        if len(tasks) == 0:
            messagebox.showinfo("Study Plan", "No tasks available.")
            return

        plan_text = ""

        for task in tasks:
            parts = task.split("|")

            if len(parts) < 4:
                continue

            title = parts[0].strip()
            subject = parts[1].strip()
            minutes_text = parts[2].replace("min", "").strip()
            deadline_text = parts[3].replace("- completed", "").strip()

            try:
                total_minutes = int(minutes_text)
                deadline = datetime.strptime(deadline_text, "%Y-%m-%d")
            except ValueError:
                continue

            days_left = (deadline - today).days + 1

            if days_left <= 0:
                days_left = 1

            minutes_per_day = total_minutes // days_left

            if total_minutes % days_left != 0:
                minutes_per_day += 1

            breaks_per_day = minutes_per_day // 50

            plan_text += f"Task: {title}\n"
            plan_text += f"Subject: {subject}\n"
            plan_text += f"Days left: {days_left}\n"
            plan_text += f"Study per day: {minutes_per_day} min\n"
            plan_text += f"Breaks per day: {breaks_per_day} x 10 min\n"
            plan_text += "----------------------\n"

        messagebox.showinfo("Study Plan", plan_text)

    def show_calendar_plan():
        calendar_window = tk.Toplevel(window)
        calendar_window.title("Study Plan Calendar")
        calendar_window.geometry("900x600")

        title = tk.Label(
            calendar_window,
            text="Study Plan Calendar",
            font=("Arial", 18)
        )
        title.pack(pady=10)

        calendar_frame = tk.Frame(calendar_window)
        calendar_frame.pack()

        today = datetime.today()
        year = today.year
        month = today.month

        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        for col in range(7):
            label = tk.Label(
                calendar_frame,
                text=days[col],
                width=16,
                height=2,
                borderwidth=1,
                relief="solid"
            )
            label.grid(row=0, column=col)

        month_calendar = calendar.monthcalendar(year, month)

        for row in range(len(month_calendar)):
            for col in range(7):
                day = month_calendar[row][col]

                text = ""
                if day != 0:
                    text = str(day)

                day_label = tk.Label(
                    calendar_frame,
                    text=text,
                    width=16,
                    height=6,
                    borderwidth=1,
                    relief="solid",
                    anchor="nw",
                    justify="left"
                )

                day_label.grid(row=row + 1, column=col)

        for task in tasks:
            parts = task.split("|")

            if len(parts) < 4:
                continue

            task_name = parts[0].strip()
            subject = parts[1].strip()
            minutes_text = parts[2].replace("min", "").strip()
            deadline_text = parts[3].replace("- completed", "").strip()

            try:
                total_minutes = int(minutes_text)
                deadline = datetime.strptime(deadline_text, "%Y-%m-%d")
            except ValueError:
                continue

            days_left = (deadline - today).days + 1

            if days_left <= 0:
                days_left = 1

            minutes_per_day = total_minutes // days_left

            if total_minutes % days_left != 0:
                minutes_per_day += 1

            breaks = minutes_per_day // 50

            for i in range(days_left):
                current_day = today.day + i

                if current_day > calendar.monthrange(year, month)[1]:
                    break

                for row in range(len(month_calendar)):
                    for col in range(7):
                        if month_calendar[row][col] == current_day:
                            old_text = calendar_frame.grid_slaves(row=row + 1, column=col)[0]["text"]

                            new_text = (
                                f"{old_text}\n\n"
                                f"{subject}\n"
                                f"{minutes_per_day} min study\n"
                                f"{breaks} break"
                            )

                            calendar_frame.grid_slaves(row=row + 1, column=col)[0]["text"] = new_text

    add_task_button = tk.Button(
        window,
        text="Add Task",
        command=add_task
    )
    add_task_button.pack(pady=8)

    complete_task_button = tk.Button(
        window,
        text="Complete Task",
        command=complete_task
    )
    complete_task_button.pack(pady=8)

    delete_task_button = tk.Button(
        window,
        text="Delete Task",
        command=delete_task
    )
    delete_task_button.pack(pady=8)

    statistics_button = tk.Button(
        window,
        text="Show Statistics",
        command=show_statistics
    )
    statistics_button.pack(pady=8)

    breaks_button = tk.Button(
        window,
        text="Study Breaks",
        command=show_break_recommendation
    )
    breaks_button.pack(pady=8)

    study_plan_button = tk.Button(
        window,
        text="Generate Study Plan",
        command=generate_study_plan
    )
    study_plan_button.pack(pady=8)

    calendar_button = tk.Button(
        window,
        text="Open Calendar Plan",
        command=show_calendar_plan
    )
    calendar_button.pack(pady=8)

    task_listbox = tk.Listbox(window, width=70)
    task_listbox.pack(pady=20)

    saved_tasks = database.get_tasks()

    for task in saved_tasks:
        task_title = task[1]
        task_subject = task[2]
        task_time = task[3]
        task_deadline = task[5]

        task_display = f"{task_title} | {task_subject} | {task_time} min | {task_deadline}"

        tasks.append(task_display)
        task_listbox.insert(tk.END, task_display)

    window.mainloop()