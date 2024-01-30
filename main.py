import tkinter as tk

def changePacking(arg):
	global createBtn, deleteBtn, nameField, confirmBtn
	if arg == 'create':
		createBtn.pack_forget()
		deleteBtn.pack_forget()
		title.config(text=f'Creating shortcut')
		nameField.pack()
		confirmBtn.config(command=lambda: create_shortcut())
		confirmBtn.pack()
	if arg == 'delete':
		createBtn.pack_forget()
		deleteBtn.pack_forget()
		title.config(text=f'Deleting shortcut')
		nameField.pack()
		confirmBtn.config(command=lambda: delete_shortcut())
		confirmBtn.pack()
	if arg == 'home':
		createBtn.pack()
		deleteBtn.pack()
		title.config(text=f'Shortcut Manager')
		nameField.pack_forget()
		confirmBtn.config(command=)
		confirmBtn.pack_forget()

def create_shortcut():
	pass

def delete_shortcut():
	pass


root = tk.Tk()
title = tk.Label(text=f'Shortcut Manager').pack()
createBtn = tk.Button(text=f'Create Shortcut', command=lambda: change_packing('create')).pack()
deleteBtn = tk.Button(text=f'Delete Shortcut', command=lambda: change_packing('delete')).pack()
nameField = tk.Entry()
confirmBtn = tk.Button(text=f'Confirm')
