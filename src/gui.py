import tkinter as tk


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

    add_task_button = tk.Button(
        window,
        text="Add Task"
    )

    add_task_button.pack(pady=10)

    statistics_button = tk.Button(
        window,
        text="Show Statistics"
    )

    statistics_button.pack(pady=10)

    window.mainloop()