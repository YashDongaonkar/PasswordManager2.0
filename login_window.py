import tkinter as tk
from tkinter import ttk, messagebox

from auth import register_user, authenticate_user
from main_app import show_main_window

def start_login_ui():
    window = tk.Tk()
    window.title("Login - Password Manager")
    window.geometry("350x220")
    window.resizable(False, False)

    def login():
        username = username_input.get().strip().lower()
        password = password_input.get()

        if not username or not password:
            messagebox.showwarning("Missing Fields", "Please fill in all fields.")
            return

        success, msg = authenticate_user(username, password)

        if success:
            messagebox.showinfo("Login", msg)
            window.destroy()
            show_main_window(username)
        else:
            messagebox.showerror("Error", msg)

    def register():
        username = username_input.get().strip().lower()
        password = password_input.get()

        if not username or not password:
            messagebox.showwarning("Missing Fields", "Please fill in all fields.")
            return

        success, msg = register_user(username, password)
        if success:
            messagebox.showinfo("Success", msg)
        else:
            messagebox.showerror("Error", msg)



    ttk.Label(window, text="Username:").pack(pady=(20, 5))
    username_input = ttk.Entry(window, width=30)
    username_input.pack()

    ttk.Label(window, text="Master Password:").pack(pady=(10, 5))
    password_input = ttk.Entry(window, show="*", width=30)
    password_input.pack()

    login_btn = ttk.Button(window, text="Login", command=login)
    login_btn.pack(pady=(15, 5))

    register_btn = ttk.Button(window, text="Register", command=register)
    register_btn.pack()

    username_input.focus()

    window.mainloop()

start_login_ui()