import tkinter as tk
from tkinter import messagebox
import json
import os

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal To-Do Manager")
        self.root.geometry("450x550")
        self.data_file = "tasks.json"
        self.tasks = self.load_data()

        # UI Setup (Demonstrating padding/margin concepts)
        self.frame = tk.Frame(root, padx=20, pady=20)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.task_entry = tk.Entry(self.frame, font=("Arial", 12))
        self.task_entry.pack(fill=tk.X, pady=10)

        self.add_button = tk.Button(self.frame, text="Add Task", command=self.add_task, bg="#4CAF50", fg="white")
        self.add_button.pack(fill=tk.X)

        self.task_listbox = tk.Listbox(self.frame, font=("Arial", 12), height=10)
        self.task_listbox.pack(fill=tk.BOTH, expand=True, pady=20)

        self.delete_button = tk.Button(self.frame, text="Delete Selected", command=self.delete_task, bg="#f44336", fg="white")
        self.delete_button.pack(fill=tk.X)

        self.refresh_listbox()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                return json.load(f)
        return []

    def save_data(self):
        with open(self.data_file, "w") as f:
            json.json.dump(self.tasks, f)

    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.tasks.append(task)
            self.save_data()
            self.refresh_listbox()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Task cannot be empty!")

    def delete_task(self):
        try:
            index = self.task_listbox.curselection()[0]
            del self.tasks[index]
            self.save_data()
            self.refresh_listbox()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to delete.")

    def refresh_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, task)

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
