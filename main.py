import tkinter as tk
from tkinter import filedialog as fd
import sqlite3 as sq
import os as os


class ShortcutManagerApp():

  def __init__(self, root):
    self.root = root
    self.root.geometry("200x400")
    self.title = tk.Label(text='Shortcut Manager')
    self.title.pack()
    
    self.con = sq.connect('locations.db')
    self.cur = self.con.cursor()
    
    self.shortFrame = tk.Frame(root)
    self.init_shortcuts(self.shortFrame)
    
    self.createBtn = tk.Button(text='Create Shortcut', command=lambda: self.change_packing('create'))
    self.createBtn.pack()
    
    self.deleteBtn = tk.Button(text='Delete Shortcut', command=lambda: self.change_packing('delete'))
    self.deleteBtn.pack()
    
    self.nameField = tk.Entry()
    self.confirmBtn = tk.Button(text='Confirm')
  
  def init_shortcuts(self, frame):
      self.cur.execute('''
      CREATE TABLE IF NOT EXISTS users (
      name TEXT NOT NULL,
      path TEXT NOT NULL	
      )
      ''')

      self.cur.execute('SELECT * FROM users')
      rows = self.cur.fetchall()
      print(rows)
      print(len(rows))
  
      for widget in frame.winfo_children():
        widget.destroy()
  
      self.cur.execute('SELECT * FROM users')  
      for row in self.cur:
        name = row[0]
        file = row[1]
        print(name,file)
        newBtn = tk.Button(frame, text=name, command=lambda path=file : os.startfile(path))
        newBtn.pack()
      frame.pack()
  
  
  def change_packing(self, arg):
    if arg == 'create':
      self.createBtn.pack_forget()
      self.shortFrame.pack_forget()
      self.deleteBtn.pack_forget()
      self.title.config(text=f'Creating shortcut')
      self.nameField.pack()
      self.confirmBtn.config(command=lambda: self.create_shortcut())
      self.confirmBtn.pack()
    if arg == 'delete':
      self.init_delete()
      self.createBtn.pack_forget()
      self.deleteBtn.pack_forget()
      self.title.config(text=f'Deleting shortcut')
      self.confirmBtn.config(command=lambda: self.delete_shortcut())
      self.confirmBtn.pack()
    if arg == 'home':
      self.init_shortcuts(self.shortFrame)
      self.createBtn.pack()
      self.deleteBtn.pack()
      self.title.config(text=f'Shortcut Manager')
      self.nameField.delete(0,tk.END)
      self.nameField.pack_forget()
      self.confirmBtn.config(command=None)
      self.confirmBtn.pack_forget()
  
  
  def create_shortcut(self):
    global nameField, con, cur
    name = self.nameField.get()
    self.cur.execute('SELECT name FROM users WHERE name = ?', (name,))
    if self.cur.fetchone():
         print('Name already exists')
         self.change_packing('home')
    else:
        file = fd.askopenfilename()
        print(f'{name}, {file}')
        self.con.execute('INSERT INTO users (name, path) VALUES (?,?)', (name, file))
        self.con.commit()
        self.change_packing('home')
  
  def init_delete(self):
      global shortFrame
      for entry in self.shortFrame.winfo_children():
          entry.configure(command=lambda text=entry.cget('text'): self.shortcut_delete(text))
  
  
  def shortcut_delete(self, name):
      global shortFrame
      self.cur.execute('DELETE FROM users WHERE name = ?', (name,))
      self.init_shortcuts(self.shortFrame)
      self.init_delete()
      print('Ran')
      self.con.commit()
  
  
  def delete_shortcut(self):
      self.cur.execute('SELECT * FROM users')
      rows = self.cur.fetchall()
      print(rows)
      print(self.shortFrame.winfo_children())
      if len(rows) > 0:
          for button in self.shortFrame.winfo_children():
                file_path = next((row[1] for row in rows if row[0] == button.cget('text')), None)
                if file_path:
                      button.configure(command=lambda path=file_path: os.startfile(path))
      self.change_packing('home')

root = tk.Tk()
ShortcutManagerApp(root)
root.mainloop()
