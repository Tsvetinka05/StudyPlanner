import tkinter as tk
from tkinter import messagebox
from src.task import Task
from src.database import Database


def start_gui():
    window = tk.Tk()
    window.title("Study Planner")
    window.geometry("500x500")

    tasks = []

    database = Database()
    database.create_tables()

    def add_task():
        task_text = task_entry.get()
        subject = subject_entry.get()
        estimated_time = int(time_entry.get())
        deadline = deadline_entry.get()

        if task_text == "":
            messagebox.showwarning("Warning", "Please enter a task.")
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

    def delete_task():
        selected_task = task_listbox.curselection()

        if not selected_task:
            messagebox.showwarning("Warning", "Please select a task.")
            return

        index = selected_task[0]

        task_listbox.delete(index)
        tasks.pop(index)
    
    def complete_task():
        selected_task = task_listbox.curselection()

        if not selected_task:
            messagebox.showwarning("Warning", "Please select a task.")
            return

        index = selected_task[0]
        task_text = tasks[index]

        tasks[index] = task_text + " - completed"

        task_listbox.delete(index)
        task_listbox.insert(index, tasks[index])

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

    task_entry = tk.Entry(window, width=30)
    task_entry.pack(pady=10)
    subject_entry = tk.Entry(window, width=30)
    subject_entry.pack(pady=5)
    subject_entry.insert(0, "Subject")

    time_entry = tk.Entry(window, width=30)
    time_entry.pack(pady=5)
    time_entry.insert(0, "Estimated minutes")

    deadline_entry = tk.Entry(window, width=30)
    deadline_entry.pack(pady=5)
    deadline_entry.insert(0, "Deadline")

    add_task_button = tk.Button(
        window,
        text="Add Task",
        command=add_task
    )
    add_task_button.pack(pady=10)
    complete_task_button = tk.Button(
    window,
    text="Complete Task",
    command=complete_task
    )
    complete_task_button.pack(pady=10)

    delete_task_button = tk.Button(
    window,
    text="Delete Task",
    command=delete_task
        )

    delete_task_button.pack(pady=10)

    statistics_button = tk.Button(
        window,
        text="Show Statistics",
        command=show_statistics
    )
    statistics_button.pack(pady=10)

    task_listbox = tk.Listbox(window, width=50)
    

    saved_tasks = database.get_tasks()

    for task in saved_tasks:
        task_title = task[1]
        tasks.append(task_title)
        task_listbox.insert(tk.END, task_title)
    
    task_listbox.pack(pady=20)

    window.mainloop()