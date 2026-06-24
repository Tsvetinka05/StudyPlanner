import tkinter as tk
from tkinter import messagebox


def start_gui():
    window = tk.Tk()
    window.title("Study Planner")
    window.geometry("500x500")

    tasks = []

    def add_task():
        task_text = task_entry.get()

        if task_text == "":
            messagebox.showwarning("Warning", "Please enter a task.")
            return

        tasks.append(task_text)
        task_listbox.insert(tk.END, task_text)
        task_entry.delete(0, tk.END)
    
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
        messagebox.showinfo(
            "Statistics",
            f"Total tasks: {len(tasks)}"
        )

    title = tk.Label(
        window,
        text="Study Planner",
        font=("Arial", 20)
    )
    title.pack(pady=20)

    task_entry = tk.Entry(window, width=30)
    task_entry.pack(pady=10)

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

    statistics_button = tk.Button(
        window,
        text="Show Statistics",
        command=show_statistics
    )
    statistics_button.pack(pady=10)

    task_listbox = tk.Listbox(window, width=50)
    task_listbox.pack(pady=20)

    window.mainloop()