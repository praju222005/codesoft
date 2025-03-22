import json
import tkinter as tk
from tkinter import messagebox

# File to store tasks
TASKS_FILE = "tasks.json"

# Load tasks from file
def load_tasks():
    try:
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Save tasks to file
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

# CLI Functions
def show_tasks(tasks):
    if not tasks:
        print("No tasks available!")
        return
    for task_id, task in tasks.items():
        status = "✔" if task["done"] else "✘"
        print(f"{task_id}: {task['name']} [{status}]")

def add_task_cli(tasks, name):
    task_id = str(len(tasks) + 1)
    tasks[task_id] = {"name": name, "done": False}
    save_tasks(tasks)

def complete_task_cli(tasks, task_id):
    if task_id in tasks:
        tasks[task_id]["done"] = True
        save_tasks(tasks)
    else:
        print("Invalid task ID!")

def delete_task_cli(tasks, task_id):
    if task_id in tasks:
        del tasks[task_id]
        save_tasks(tasks)
    else:
        print("Invalid task ID!")

def cli_mode():
    tasks = load_tasks()
    while True:
        print("\n1. Add Task\n2. Show Tasks\n3. Complete Task\n4. Delete Task\n5. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Enter task name: ")
            add_task_cli(tasks, name)
        elif choice == "2":
            show_tasks(tasks)
        elif choice == "3":
            task_id = input("Enter task ID to mark as complete: ")
            complete_task_cli(tasks, task_id)
        elif choice == "4":
            task_id = input("Enter task ID to delete: ")
            delete_task_cli(tasks, task_id)
        elif choice == "5":
            break
        else:
            print("Invalid choice, try again!")

# GUI Functions
tasks = load_tasks()

def add_task():
    task = entry.get()
    if task:
        task_id = str(len(tasks) + 1)
        tasks[task_id] = {"name": task, "done": False}
        save_tasks(tasks)
        listbox.insert(tk.END, task)
        entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Task cannot be empty!")

def delete_task():
    try:
        index = listbox.curselection()[0]
        task_id = str(index + 1)
        del tasks[task_id]
        save_tasks(tasks)
        listbox.delete(index)
    except IndexError:
        messagebox.showwarning("Warning", "No task selected!")

def complete_task():
    try:
        index = listbox.curselection()[0]
        task_id = str(index + 1)
        tasks[task_id]["done"] = True
        save_tasks(tasks)
        listbox.itemconfig(index, {'fg': 'green'})
    except IndexError:
        messagebox.showwarning("Warning", "No task selected!")

def gui_mode():
    global entry, listbox

    root = tk.Tk()
    root.title("To-Do List")

    frame = tk.Frame(root)
    frame.pack(pady=10)

    entry = tk.Entry(frame, width=40)
    entry.pack(side=tk.LEFT)

    add_button = tk.Button(frame, text="Add", command=add_task)
    add_button.pack(side=tk.LEFT)

    listbox = tk.Listbox(root, width=50, height=10)
    listbox.pack(pady=10)

    for task in tasks.values():
        listbox.insert(tk.END, task["name"])

    btn_frame = tk.Frame(root)
    btn_frame.pack()

    complete_button = tk.Button(btn_frame, text="Complete", command=complete_task)
    complete_button.pack(side=tk.LEFT, padx=5)

    delete_button = tk.Button(btn_frame, text="Delete", command=delete_task)
    delete_button.pack(side=tk.LEFT, padx=5)

    root.mainloop()

# Run CLI or GUI
if __name__ == "__main__":
    mode = input("Enter mode (CLI/GUI): ").strip().lower()
    if mode == "cli":
        cli_mode()
    elif mode == "gui":
        gui_mode()
    else:
        print("Invalid mode! Choose 'CLI' or 'GUI'.")
