import tkinter as tk
import calendar
from tkinter import messagebox
from datetime import datetime, timedelta

from src.task import Task
from src.database import Database


def start_gui():
    window = tk.Tk()
    window.title("Study Planner")
    window.geometry("700x750")

    tasks = []
    completed_today = []

    database = Database()
    database.create_tables()

    def clear_placeholder(entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)

    def add_placeholder(entry, placeholder):
        if entry.get() == "":
            entry.insert(0, placeholder)

    def parse_task(task_text):
        parts = task_text.split("|")

        if len(parts) < 4:
            return None

        title = parts[0].strip()
        subject = parts[1].strip()
        minutes_text = parts[2].replace("min", "").strip()
        deadline = parts[3].replace("- completed", "").strip()

        if not minutes_text.isdigit():
            return None

        return {
            "title": title,
            "subject": subject,
            "minutes": int(minutes_text),
            "deadline": deadline,
            "completed": "completed" in task_text
        }

    def refresh_listbox():
        task_listbox.delete(0, tk.END)

        for task in tasks:
            task_listbox.insert(tk.END, task)

    def update_dashboard():
        completed = 0
        remaining_time = 0
        today_time = get_today_study_time()

        for task in tasks:
            info = parse_task(task)

            if info is None:
                continue

            if info["completed"]:
                completed += 1
            else:
                remaining_time += info["minutes"]

        pending = len(tasks) - completed

        tasks_card.config(text=f"Tasks: {len(tasks)}")
        completed_card.config(text=f"Completed: {completed}")
        pending_card.config(text=f"Pending: {pending}")
        remaining_card.config(text=f"Remaining: {remaining_time} min")
        today_card.config(text=f"Today: {today_time} min")

    def get_today_study_time():
        today_key = datetime.today().strftime("%Y-%m-%d")
        plan = build_smart_plan()

        if today_key not in plan:
            return 0

        total = 0

        for item in plan[today_key]:
            total += item["minutes"]

        return total

    def update_today_focus():
        today_key = datetime.today().strftime("%Y-%m-%d")
        plan = build_smart_plan()

        if today_key not in plan or len(plan[today_key]) == 0:
            focus_label.config(text="Today's Focus: No active tasks")
            return

        best_item = plan[today_key][0]

        focus_label.config(
            text=(
                f"Today's Focus: {best_item['title']} | "
                f"{best_item['subject']} | "
                f"{best_item['minutes']} min today"
            )
        )

    def refresh_info():
        update_dashboard()
        update_today_focus()

    def build_smart_plan():
        today = datetime.today()
        daily_plan = {}

        for task in tasks:
            info = parse_task(task)

            if info is None or info["completed"]:
                continue

            try:
                deadline = datetime.strptime(info["deadline"], "%Y-%m-%d")
            except ValueError:
                continue

            days_left = (deadline - today).days + 1

            if days_left <= 0:
                days_left = 1

            minutes_per_day = info["minutes"] // days_left

            if info["minutes"] % days_left != 0:
                minutes_per_day += 1

            remaining = info["minutes"]

            for i in range(days_left):
                current_date = today + timedelta(days=i)
                current_key = current_date.strftime("%Y-%m-%d")

                minutes_for_day = minutes_per_day

                if minutes_for_day > remaining:
                    minutes_for_day = remaining

                if minutes_for_day <= 0:
                    break

                if current_key not in daily_plan:
                    daily_plan[current_key] = []

                breaks = minutes_for_day // 50

                daily_plan[current_key].append({
                    "title": info["title"],
                    "subject": info["subject"],
                    "minutes": minutes_for_day,
                    "breaks": breaks,
                    "deadline": info["deadline"]
                })

                remaining -= minutes_for_day

        return daily_plan

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

        task = Task(task_text, subject, estimated_time, 1, deadline)
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

        refresh_info()

        messagebox.showinfo("Success", "Task added successfully!")

    def complete_task():
        selected_task = task_listbox.curselection()

        if not selected_task:
            messagebox.showwarning("Warning", "Please select a task.")
            return

        index = selected_task[0]
        task_text = tasks[index]

        if "completed" in task_text:
            return

        task_title = task_text.split("|")[0].strip()
        database.complete_task_by_title(task_title)

        tasks[index] = task_text + " - completed"

        refresh_listbox()
        refresh_info()

        messagebox.showinfo("Success", "Task completed successfully!")

    def complete_today_work():
        today_key = datetime.today().strftime("%Y-%m-%d")
        plan = build_smart_plan()

        if today_key not in plan or len(plan[today_key]) == 0:
            messagebox.showinfo("Today", "No study work planned for today.")
            return

        today_task = plan[today_key][0]

        task_title = today_task["title"]
        minutes_done = today_task["minutes"]

        today_key = datetime.today().strftime("%Y-%m-%d")
        completed_key = task_title + "|" + today_key

        if completed_key in completed_today:
            messagebox.showwarning(
                "Warning",
                "You have already completed today's work for this task."
            )
            return

        completed_today.append(completed_key)

        for i in range(len(tasks)):
            info = parse_task(tasks[i])

            if info is None:
                continue

            if info["title"] == task_title and not info["completed"]:
                new_minutes = info["minutes"] - minutes_done

                database.delete_task_by_title(task_title)

                if new_minutes <= 0:
                    completed_task = Task(
                        info["title"],
                        info["subject"],
                        0,
                        1,
                        info["deadline"]
                    )

                    database.add_task(completed_task)
                    database.complete_task_by_title(info["title"])

                    tasks[i] = (
                        f"{info['title']} | "
                        f"{info['subject']} | "
                        f"0 min | "
                        f"{info['deadline']} - completed"
                    )

                    messagebox.showinfo(
                        "Success",
                        f"Today's work is completed.\nThe whole task '{task_title}' is now completed."
                    )
                else:
                    updated_task = Task(
                        info["title"],
                        info["subject"],
                        new_minutes,
                        1,
                        info["deadline"]
                    )

                    database.add_task(updated_task)

                    tasks[i] = (
                        f"{info['title']} | "
                        f"{info['subject']} | "
                        f"{new_minutes} min | "
                        f"{info['deadline']}"
                    )

                    messagebox.showinfo(
                        "Success",
                        f"Today's work is completed.\nRemaining time for '{task_title}': {new_minutes} min."
                    )

                refresh_listbox()
                refresh_info()
                return

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

        refresh_info()

    def show_statistics():
        completed = 0
        remaining_time = 0

        for task in tasks:
            info = parse_task(task)

            if info is None:
                continue

            if info["completed"]:
                completed += 1
            else:
                remaining_time += info["minutes"]

        pending = len(tasks) - completed

        messagebox.showinfo(
            "Statistics",
            f"Total tasks: {len(tasks)}\n"
            f"Completed: {completed}\n"
            f"Pending: {pending}\n"
            f"Remaining study time: {remaining_time} min\n"
            f"Today's study time: {get_today_study_time()} min"
        )

    def show_break_recommendation():
        today_minutes = get_today_study_time()

        if today_minutes == 0:
            messagebox.showinfo("Study Breaks", "No study time available for today.")
            return

        breaks = today_minutes // 50

        messagebox.showinfo(
            "Study Breaks",
            f"Today's study time: {today_minutes} minutes\n"
            f"Recommended breaks: {breaks}\n\n"
            "Recommendation: Take a 10 minute break after every 50 minutes of studying."
        )

    def generate_study_plan():
        plan = build_smart_plan()

        if len(plan) == 0:
            messagebox.showinfo("Study Plan", "No active tasks available.")
            return

        plan_text = ""

        for day in sorted(plan):
            day_total = 0

            for item in plan[day]:
                day_total += item["minutes"]

            plan_text += f"{day} | Total: {day_total} min\n"

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
                    height=7,
                    borderwidth=1,
                    relief="solid",
                    anchor="nw",
                    justify="left"
                )

                day_label.grid(row=row + 1, column=col)

        plan = build_smart_plan()

        for day_key in plan:
            day_date = datetime.strptime(day_key, "%Y-%m-%d")

            if day_date.month != month or day_date.year != year:
                continue

            day = day_date.day

            for row in range(len(month_calendar)):
                for col in range(7):
                    if month_calendar[row][col] == day:
                        cell = calendar_frame.grid_slaves(
                            row=row + 1,
                            column=col
                        )[0]

                        old_text = cell["text"]

                        text_for_day = ""

                        for item in plan[day_key]:
                            text_for_day += (
                                f"{item['subject']}: "
                                f"{item['minutes']} min, "
                                f"{item['breaks']} break\n"
                            )

                        cell["text"] = f"{old_text}\n\n{text_for_day}"

    title = tk.Label(
        window,
        text="Study Planner",
        font=("Arial", 20)
    )
    title.pack(pady=15)

    dashboard_frame = tk.Frame(window)
    dashboard_frame.pack(pady=5)

    tasks_card = tk.Label(dashboard_frame, text="Tasks: 0", width=18, relief="ridge")
    tasks_card.grid(row=0, column=0, padx=3, pady=3)

    completed_card = tk.Label(dashboard_frame, text="Completed: 0", width=18, relief="ridge")
    completed_card.grid(row=0, column=1, padx=3, pady=3)

    pending_card = tk.Label(dashboard_frame, text="Pending: 0", width=18, relief="ridge")
    pending_card.grid(row=1, column=0, padx=3, pady=3)

    remaining_card = tk.Label(dashboard_frame, text="Remaining: 0 min", width=18, relief="ridge")
    remaining_card.grid(row=1, column=1, padx=3, pady=3)

    today_card = tk.Label(dashboard_frame, text="Today: 0 min", width=18, relief="ridge")
    today_card.grid(row=2, column=0, columnspan=2, padx=3, pady=3)

    focus_label = tk.Label(
        window,
        text="Today's Focus: No active tasks",
        font=("Arial", 11)
    )
    focus_label.pack(pady=5)

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

    add_task_button = tk.Button(window, text="Add Task", command=add_task)
    add_task_button.pack(pady=5)

    complete_today_button = tk.Button(
        window,
        text="Complete Today's Work",
        command=complete_today_work
    )
    complete_today_button.pack(pady=5)

    complete_task_button = tk.Button(window, text="Complete Whole Task", command=complete_task)
    complete_task_button.pack(pady=5)

    delete_task_button = tk.Button(window, text="Delete Task", command=delete_task)
    delete_task_button.pack(pady=5)

    statistics_button = tk.Button(window, text="Show Statistics", command=show_statistics)
    statistics_button.pack(pady=5)

    breaks_button = tk.Button(window, text="Study Breaks", command=show_break_recommendation)
    breaks_button.pack(pady=5)

    study_plan_button = tk.Button(window, text="Generate Study Plan", command=generate_study_plan)
    study_plan_button.pack(pady=5)

    calendar_button = tk.Button(window, text="Open Calendar Plan", command=show_calendar_plan)
    calendar_button.pack(pady=5)

    task_listbox = tk.Listbox(window, width=80)
    task_listbox.pack(pady=15)

    saved_tasks = database.get_tasks()

    for task in saved_tasks:
        task_title = task[1]
        task_subject = task[2]
        task_time = task[3]
        task_deadline = task[5]
        completed = task[6]

        task_display = (
            f"{task_title} | "
            f"{task_subject} | "
            f"{task_time} min | "
            f"{task_deadline}"
        )

        if completed == 1:
            task_display += " - completed"

        tasks.append(task_display)
        task_listbox.insert(tk.END, task_display)

    refresh_info()

    window.mainloop()