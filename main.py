import tkinter as tk
from tkinter import filedialog as fd
import sqlite3 as sq
import os as os

loc_path = os.path.join(os.path.dirname(__file__), 'locations.db')
con = sq.connect(loc_path)
print('db opened')
cur = con.cursor()
print('Cursor Initiated')
cur.execute('''
CREATE TABLE IF NOT EXISTS users (
name TEXT NOT NULL,
path TEXT NOT NULL	
)
''')
# print('Table created')

# cur.execute('INSERT INTO users (name, path) VALUES (?,?)', ('Test', '"C:/Users/19gtaylor/OneDrive - Blackdown Education Partnership/Programming/accounts.txt"'))

cur.execute('SELECT * FROM users')
rows = cur.fetchall()

def init_shortcuts(frame):
    cur.execute('SELECT * FROM users')
    rows = cur.fetchall()
    print(f'Len rows {len(rows)}, len frame {len(shortFrame.winfo_children())}')
    
    if len(frame.winfo_children()) == 0 and len(rows) > 0:
        for i in range (0,len(rows)):
                rowid = i
                #print(i)
                cur.execute('SELECT * FROM users WHERE rowid = ?', (rowid+1,))
                result = cur.fetchone()
                #print(result)
                if result:
                    name = result[0]
                    file = result[1]
                    print(name,file)
                    newBtn = tk.Button(shortFrame, text=name, command=lambda: os.startfile(file))
                    newBtn.pack()
        shortFrame.pack()

    elif len(frame.winfo_children()) == len(rows):
        shortFrame.pack()

    elif len(frame.winfo_children()) < len(rows):
        for i in range (len(frame.winfo_children()), len(rows)):
            rowid = i
            cur.execute('SELECT * FROM users WHERE rowid = ?', (rowid+1,))
            result = cur.fetchone()
            if result:
                name = result[0]
                file = result[1]
                print(name,file)
                newBtn = tk.Button(shortFrame, text=name, command=lambda: os.startfile(file))
                newBtn.pack()
        shortFrame.pack()
    else:
        pass

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
    cur.execute('SELECT name FROM users WHERE name = ?', name)
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
    for entry in shortFrame.winfo_children():
        print(f'assigning button {entry.cget("text")}')
        entry.configure(text=entry.cget('text'), command=lambda: shortcut_delete(entry.cget('text')))
	
		
def shortcut_delete(name):
    print(f'NAME BEING DELETED: {name}')
    cur.execute('DELETE FROM users WHERE name = ?', (name,))
    con.commit()
    for widget in shortFrame.winfo_children():
          widget.destroy()
    cur.execute('SELECT * FROM users')
    rows = cur.fetchall()
    if len(rows) > 0:
        for i in range (0,len(rows)):
                rowid = i
                #print(i)
                cur.execute('SELECT * FROM users WHERE rowid = ?', (rowid+1,))
                result = cur.fetchone()
                #print(result)
                if result:
                    name = result[0]
                    file = result[1]
                    print(name,file)
                    newBtn = tk.Button(shortFrame, text=name, command=lambda: os.startfile(file))
                    newBtn.pack()
    print('Ran')
    
	

def delete_shortcut():
    cur.execute('SELECT * FROM users')
    rows = cur.fetchall()
    print(rows)
    print(shortFrame.winfo_children())
    
    
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
