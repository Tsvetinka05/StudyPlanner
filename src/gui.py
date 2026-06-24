import tkinter as tk


def start_gui():
    window = tk.Tk()
    window.title("Study Planner")
    window.geometry("500x400")

    title = tk.Label(window, text="Study Planner", font=("Arial", 20))
    title.pack(pady=20)

    window.mainloop()