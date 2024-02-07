import tkinter as tk
from tkinter import filedialog as fd
import sqlite3 as sq
import os as os

con = sq.connect('locations.db')
print('db opened')
cur = con.cursor()
print('Cursor Initiated')
cur.execute('''
CREATE TABLE IF NOT EXISTS users (
name TEXT NOT NULL,
path TEXT NOT NULL	
)
''')

cur.execute('SELECT * FROM users')
rows = cur.fetchall()

def init_shortcuts(frame):
    cur.execute('SELECT * FROM users')
    rows = cur.fetchall()
    print(rows)
    print(len(rows))

    for widget in frame.winfo_children():
      widget.destroy()
  
    cur.execute('SELECT * FROM users')  
    for row in cur:
      name = row[0]
      file = row[1]
      print(name,file)
      newBtn = tk.Button(frame, text=name, command=lambda path=file : os.startfile(path))
      newBtn.pack()
      frame.pack()
        

def change_packing(arg):
  global createBtn, deleteBtn, nameField, confirmBtn, newBtn
  if arg == 'create':
    createBtn.pack_forget()
    shortFrame.pack_forget()
    deleteBtn.pack_forget()
    title.config(text=f'Creating shortcut')
    nameField.pack()
    confirmBtn.config(command=lambda: create_shortcut())
    confirmBtn.pack()
  if arg == 'delete':
    init_delete()
    createBtn.pack_forget()
    deleteBtn.pack_forget()
    title.config(text=f'Deleting shortcut')
    confirmBtn.config(command=lambda: delete_shortcut())
    confirmBtn.pack()
  if arg == 'home':
    init_shortcuts(shortFrame)
    createBtn.pack()
    deleteBtn.pack()
    title.config(text=f'Shortcut Manager')
    nameField.delete(0,tk.END)
    nameField.pack_forget()
    confirmBtn.config(command=None)
    confirmBtn.pack_forget()


def create_shortcut():
  global nameField, con, cur
  name = nameField.get()
  cur.execute('SELECT name FROM users WHERE name = ?', (name,))
  if cur.fetchone():
       print('Name already exists')
       change_packing('home')
  else:
      file = fd.askopenfilename()
      print(f'{name}, {file}')
      con.execute('INSERT INTO users (name, path) VALUES (?,?)', (name, file))
      con.commit()
      change_packing('home')

def init_delete():
    global shortFrame
    for entry in shortFrame.winfo_children():
        entry.configure(command=lambda text=entry.cget('text'): shortcut_delete(text))


def shortcut_delete(name):
    global shortFrame
    cur.execute('DELETE FROM users WHERE name = ?', (name,))
    init_shortcuts(shortFrame)
    print('Ran')
    con.commit()


def delete_shortcut():
    cur.execute('SELECT * FROM users')
    rows = cur.fetchall()
    print(rows)
    print(shortFrame.winfo_children())


    if len(rows) > 0:
        for button in shortFrame.winfo_children():
              file_path = next((row[1] for row in rows if row[0] == button.cget('text')), None)
              if file_path:
                    button.configure(command=lambda path=file_path: os.startfile(path))
    change_packing('home')

root = tk.Tk()
root.geometry("200x400")
title = tk.Label(text=f'Shortcut Manager')
title.pack()
shortFrame = tk.Frame(root)
# init_shortcuts(shortFrame)
init_shortcuts(shortFrame)
createBtn = tk.Button(text=f'Create Shortcut', command=lambda: change_packing('create'))
createBtn.pack()
deleteBtn = tk.Button(text=f'Delete Shortcut', command=lambda: change_packing('delete'))
deleteBtn.pack()
nameField = tk.Entry()
confirmBtn = tk.Button(text=f'Confirm')
root.mainloop()

root.geometry("200x100")
title = tk.Label(text=f'Shortcut Manager')
title.pack()
shortFrame = tk.Frame(root)
# init_shortcuts(shortFrame)
init_shortcuts(shortFrame)
createBtn = tk.Button(text=f'Create Shortcut', command=lambda: change_packing('create'))
createBtn.pack()
deleteBtn = tk.Button(text=f'Delete Shortcut', command=lambda: change_packing('delete'))
deleteBtn.pack()
nameField = tk.Entry()
confirmBtn = tk.Button(text=f'Confirm')
root.mainloop()
