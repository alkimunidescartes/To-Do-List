import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Connect to the database
def connect_to_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Goal2012",
            database="todo_list_db")
    except mysql.connector.Error as err:
        messagebox.showerror("Connection Error", f"Error: {err}")
        return None 

# CRUD Functions
def create_task(task_name, due_date, priority):
    connection = connect_to_db()
    cursor = connection.cursor()
    sql = "INSERT INTO tasks (task_name, due_date, priority) VALUES (%s, %s, %s)"
    cursor.execute(sql, (task_name, due_date, priority))
    connection.commit()
    connection.close()
    messagebox.showinfo("Success", "Task added successfully!")
    load_tasks()

def get_all_tasks():
    connection = connect_to_db()
    if connection is None:
        return []
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT task_id, task_name, status, due_date, priority FROM tasks")
        tasks = cursor.fetchall()
    except mysql.connector.Error as err:
        messagebox.showerror("Query Error", f"Error: {err}")
        tasks = []
    finally:
        connection.close()
    return tasks  

def update_task_status(task_id, new_status):
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("UPDATE tasks SET status = %s WHERE task_id = %s", (new_status, task_id))
    connection.commit()
    connection.close()
    print(f"Task ID {task_id} status updated to {new_status}!")

def delete_task(task_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM tasks WHERE task_id = %s", (task_id,))
    connection.commit()
    connection.close()
    print(f"Task ID {task_id} deleted successfully!")
    load_tasks()

# GUI Functions
def load_tasks():
    tasks = get_all_tasks()
    listbox.delete(0, tk.END)  
    for task in tasks:
        task_str = f"ID: {task[0]}, Task: {task[1]}, Status: {task[2]}, Due: {task[3]}, Priority: {task[4]}"
        if task[4] == 'High':
            listbox.insert(tk.END, task_str)
            listbox.itemconfig(tk.END, {'fg': 'red'})
        elif task[4] == 'Medium':
            listbox.insert(tk.END, task_str)
            listbox.itemconfig(tk.END, {'fg': 'orange'})
        else:
            listbox.insert(tk.END, task_str)
            listbox.itemconfig(tk.END, {'fg': 'yellow'})

def add_task():
    task_name = entry_task_name.get()
    due_date = entry_due_date.get()
    priority = entry_priority.get()
    create_task(task_name, due_date, priority)

def update_task():
    selected_task = listbox.curselection()
    if not selected_task:
        messagebox.showwarning("Select a task", "Please select a task to update.")
        return
    task_id = get_all_tasks()[selected_task[0]][0]
    new_status = entry_status.get()
    update_task_status(task_id, new_status)

def delete_selected_task():
    selected_task = listbox.curselection()
    if not selected_task:
        messagebox.showwarning("Select a task", "Please select a task to delete.")
        return
    task_id = get_all_tasks()[selected_task[0]][0]
    delete_task(task_id)

def search_tasks():
    search_term = entry_search.get().lower()
    tasks = get_all_tasks()
    listbox.delete(0, tk.END)
    for task in tasks:
        if search_term in task[1].lower():
            task_str = f"ID: {task[0]}, Task: {task[1]}, Status: {task[2]}, Due: {task[3]}, Priority: {task[4]}"
            listbox.insert(tk.END, task_str)
    if listbox.size() == 0:
        listbox.insert(tk.END, "No tasks found.")

# Add close and minimize functions
def close_app():
    root.quit()  

def hide_app():
    root.iconify()  

# Setting up the Tkinter GUI
root = tk.Tk()
root.title("To-Do List App")
root.geometry("800x600")  # Set initial size
root.minsize(600, 400)    # Minimum window size

# Configure grid to make widgets responsive
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(1, weight=1)

# Close and minimize buttons at the top right
close_button = tk.Button(root, text="X", command=close_app, font=('Helvetica', 10), bg='red', fg='white', width=2)
close_button.place(x=root.winfo_screenwidth() - 30, y=5)

hide_button = tk.Button(root, text="_", command=hide_app, font=('Helvetica', 10), bg='gray', fg='white', width=2)
hide_button.place(x=root.winfo_screenwidth() - 60, y=5)

# Font and style settings
font_style = ('Helvetica', 12, 'bold')

# Search Bar at the top
search_label = tk.Label(root, text="Search Task:", font=('Helvetica', 12))
search_label.grid(row=0, column=0, padx=10, pady=(15, 5), sticky='nw')

entry_search = tk.Entry(root, font=('Helvetica', 12))
entry_search.grid(row=0, column=1, padx=10, pady=(15, 5), sticky='nsew')

search_button = tk.Button(root, text="Search", command=search_tasks, font=('Helvetica', 12), bg='blue', fg='white')
search_button.grid(row=0, column=2, padx=10, pady=(15, 5))

# Task display (Listbox)
listbox = tk.Listbox(root, font=font_style)
listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

# Scrollbar for Listbox
scrollbar = tk.Scrollbar(root, command=listbox.yview)
scrollbar.grid(row=1, column=3, sticky='ns')
listbox.config(yscrollcommand=scrollbar.set)

# Task Form
tk.Label(root, text="Task Name", font=font_style).grid(row=2, column=0, padx=10, pady=5, sticky='w')
entry_task_name = tk.Entry(root, font=font_style)
entry_task_name.grid(row=2, column=1, padx=10, pady=5, sticky='ew')

tk.Label(root, text="Due Date (YYYY-MM-DD)", font=font_style).grid(row=3, column=0, padx=10, pady=5, sticky='w')
entry_due_date = tk.Entry(root, font=font_style)
entry_due_date.grid(row=3, column=1, padx=10, pady=5, sticky='ew')

tk.Label(root, text="Priority (High, Medium, Low)", font=font_style).grid(row=4, column=0, padx=10, pady=5, sticky='w')
entry_priority = tk.Entry(root, font=font_style)
entry_priority.grid(row=4, column=1, padx=10, pady=5, sticky='ew')

tk.Label(root, text="Update Status (Pending, Completed)", font=font_style).grid(row=5, column=0, padx=10, pady=5, sticky='w')
entry_status = tk.Entry(root, font=font_style)
entry_status.grid(row=5, column=1, padx=10, pady=5, sticky='ew')

# Action Buttons
tk.Button(root, text="Add Task", command=add_task, font=font_style, bg='lightblue').grid(row=6, column=0, padx=10, pady=15, sticky='ew')
tk.Button(root, text="Update Task", command=update_task, font=font_style, bg='lightgreen').grid(row=6, column=1, padx=10, pady=15, sticky='ew')
tk.Button(root, text="Delete Task", command=delete_selected_task, font=font_style, bg='lightcoral').grid(row=6, column=2, padx=10, pady=15, sticky='ew')

# Load tasks when starting
load_tasks()

# Start the Tkinter event loop
root.mainloop()
