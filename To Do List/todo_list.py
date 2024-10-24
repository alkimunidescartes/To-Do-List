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
        messagebox.showerror("Connection Error",f"Error: {err}")
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
    load_tasks()  # Refresh the task list

def get_all_tasks():
    connection = connect_to_db()
    if connection is None:
        return []
    cursor = connection.cursor()
    try: 
        cursor.execute("SELECT task_id, task_name, status, due_date, priority FROM tasks")
        tasks = cursor.fetchall()
    except mysql.connector.Error as err:
        messagebox.showerror("Query Error",f"Error:{err}")
        tasks=[]
    finally:
        connection.close()
    return tasks  # Ensure this line is present


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
    listbox.delete(0, tk.END)  # Clear the current list
    for task in tasks:
        
        task_str = f"ID: {task[0]}, Task: {task[1]}, Status: {task[2]}, Due: {task[3]}, Priority: {task[4]}"
        # Set task color based on priority
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
    task_id = get_all_tasks()[selected_task[0]][0]  # Get ID of the selected task
    new_status = entry_status.get()
    update_task_status(task_id, new_status)

def delete_selected_task():
    selected_task = listbox.curselection()
    if not selected_task:
        messagebox.showwarning("Select a task", "Please select a task to delete.")
        return
    task_id = get_all_tasks()[selected_task[0]][0]  # Get ID of the selected task
    delete_task(task_id)

# Add "Close" and "Hide" functionality
def close_app():
    root.quit()  # Close the Tkinter window

def hide_app():
    root.iconify()  # Minimize the Tkinter window
    
# Setting up the Tkinter GUI
root = tk.Tk()
root.title("To-Do List App")
root.attributes("-fullscreen",True)

# Create GUI elements with fonts and styling
font_style = ('Helvetica', 12, 'bold')

# Task display (Listbox)
listbox = tk.Listbox(root, width=120, height=40, font=font_style)
listbox.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

# Ensure that the Close and Hide buttons remain on top-right and are not affected by the Listbox
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(0, weight=1)

scrollbar = tk.Scrollbar(root)
scrollbar.grid(row=0, column=3, sticky='ns')
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

# Task form
tk.Label(root, text="Task Name", font=font_style).grid(row=1, column=0, padx=10, pady=5, sticky='w')
entry_task_name = tk.Entry(root, font=font_style)
entry_task_name.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Due Date (YYYY-MM-DD)", font=font_style).grid(row=2, column=0, padx=10, pady=5, sticky='w')
entry_due_date = tk.Entry(root, font=font_style)
entry_due_date.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Priority (High, Medium, Low)", font=font_style).grid(row=3, column=0, padx=10, pady=5, sticky='w')
entry_priority = tk.Entry(root, font=font_style)
entry_priority.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Update Status (Pending, Completed)", font=font_style).grid(row=4, column=0, padx=10, pady=5, sticky='w')
entry_status = tk.Entry(root, font=font_style)
entry_status.grid(row=4, column=1, padx=10, pady=5)

# Buttons
tk.Button(root, text="Add Task", command=add_task, font=font_style, bg='lightblue').grid(row=5, column=0, padx=10, pady=5, sticky='ew')
tk.Button(root, text="Update Task", command=update_task, font=font_style, bg='lightgreen').grid(row=5, column=1, padx=10, pady=5, sticky='ew')
tk.Button(root, text="Delete Task", command=delete_selected_task, font=font_style, bg='lightcoral').grid(row=5, column=2, padx=10, pady=5, sticky='ew')

# Close and Hide buttons (small, top-right corner)
close_button = tk.Button(root, text="X", command=close_app, font=('Helvetica', 10), bg='red', fg='white', width=2)
close_button.place(x=root.winfo_screenwidth()-30, y=5)

hide_button = tk.Button(root, text="_", command=hide_app, font=('Helvetica', 10), bg='orange', fg='white', width=2)
hide_button.place(x=root.winfo_screenwidth()-60, y=5)


# Make the window grid layout responsive
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(0, weight=1)

# Load tasks when starting
load_tasks()

# Start the Tkinter event loop
root.mainloop()