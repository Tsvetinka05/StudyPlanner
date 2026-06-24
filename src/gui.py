import tkinter as tk
from tkinter import messagebox

def start_gui():
    window = tk.Tk()
    window.title("Study Planner")
    window.geometry("500x400")

    title = tk.Label(
        window,
        text="Study Planner",
        font=("Arial", 20)
    )

    title.pack(pady=20)

    task_entry = tk.Entry(
    window,
    width=30
    )

    task_entry.pack(pady=10)

    add_task_button = tk.Button(
        window,
        text="Add Task"
    )

    add_task_button.pack(pady=10)

    statistics_button = tk.Button(
    window,
    text="Show Statistics",
    command=show_statistics
    )

    statistics_button.pack(pady=10)

    window.mainloop()


def show_statistics():
    messagebox.showinfo(
        "Statistics",
        "Statistics will be shown here."
    )