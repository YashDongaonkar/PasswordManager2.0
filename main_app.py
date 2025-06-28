import tkinter as tk
from tkinter import ttk, messagebox
from random import choice, randint, shuffle
import re, math

from crypto_utils import encrypt, decrypt
from db_utils import vaults_col

def show_main_window(username):
    window = tk.Tk()
    window.title(f"Vault - {username}")
    window.config(padx=40, pady=40)

    def generate_password():
        letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        digits = "0123456789"
        symbols = "!#$%&()*+"

        pswd_list = (
            [choice(letters) for _ in range(randint(8, 10))] +
            [choice(digits) for _ in range(randint(2, 4))] +
            [choice(symbols) for _ in range(randint(2, 4))]
        )
        shuffle(pswd_list)
        pswd = ''.join(pswd_list)

        password_input.delete(0, tk.END)
        password_input.insert(0, pswd)
        window.clipboard_clear()
        window.clipboard_append(pswd)
        update_strength_bar()

    def estimate_entropy(password):
        charset = 0
        if re.search(r"[a-z]", password): charset += 26
        if re.search(r"[A-Z]", password): charset += 26
        if re.search(r"[0-9]", password): charset += 10
        if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): charset += 32
        if charset == 0: return 0
        return round(len(password) * math.log2(charset), 2)

    def update_strength_bar():
        pswd = password_input.get()
        entropy = estimate_entropy(pswd)
        entropy_bar['value'] = min(entropy, 100)
        if entropy < 40:
            entropy_label_var.set("Weak")
        elif entropy < 70:
            entropy_label_var.set("Medium")
        else:
            entropy_label_var.set("Strong")
        entropy_value_var.set(f"{entropy} bits")

    
    def save_entry():
        website = website_input.get().strip().title()
        email = email_input.get().strip().lower()
        password = password_input.get().strip()

        if not website or not password or not email:
            messagebox.showerror("Missing Info", "Empty Entries")
            return

        encrypted_pswd = encrypt(password)

        vaults_col.update_one(
            {"owner": username, "website": website, "email": email},
            {"$set": {"password": encrypted_pswd}},
            upsert=True
        )

        website_input.delete(0, tk.END)
        password_input.delete(0, tk.END)
        entropy_label_var.set("")
        entropy_value_var.set("")
        window.clipboard_clear()
        window.clipboard_append(password)
        messagebox.showinfo("Saved", "Password saved and copied to clipboard.")

    def search_entry():
        website = website_input.get().strip().title()
        email = email_input.get().strip().lower()

        if not website or not email:
            messagebox.showerror("Missing Input", "Enter both website and email to search.")
            return

        entry = vaults_col.find_one({
            "owner": username,
            "website": website,
            "email": email
        })

        if not entry:
            messagebox.showerror("Not Found", f"No entry for {website} and {email}")
            return

        try:
            decrypted_pswd = decrypt(entry["password"])
        except:
            messagebox.showerror("Error", "Decryption failed.")
            return

        messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {decrypted_pswd}")
        window.clipboard_clear()
        window.clipboard_append(decrypted_pswd)

    def grid(widget, r, c, colspan=1):
        widget.grid(row=r, column=c, columnspan=colspan, sticky="w", pady=5)

    website_label = ttk.Label(text="Website:")
    website_input = ttk.Entry(width=22)

    email_label = ttk.Label(text="Email:")
    email_input = ttk.Entry(width=35)

    password_label = ttk.Label(text="Password:")
    password_input = ttk.Entry(width=22, show="*")
    password_input.bind("<KeyRelease>", update_strength_bar)

    search_button = ttk.Button(text="Search", command=search_entry)
    generate_button = ttk.Button(text="Generate", command=generate_password)
    add_button = ttk.Button(text="Save", width=34, command=save_entry)

    entropy_label_var = tk.StringVar()
    entropy_value_var = tk.StringVar()
    entropy_label = ttk.Label(textvariable=entropy_label_var)
    entropy_value = ttk.Label(textvariable=entropy_value_var)
    entropy_bar = ttk.Progressbar(length=200, maximum=100)

    grid(website_label, 0, 0)
    grid(website_input, 0, 1)
    grid(search_button, 0, 2)

    grid(email_label, 1, 0)
    grid(email_input, 1, 1, colspan=2)

    grid(password_label, 2, 0)
    grid(password_input, 2, 1)
    grid(generate_button, 2, 2)

    grid(entropy_label, 3, 1)
    grid(entropy_value, 3, 2)
    grid(entropy_bar, 4, 1, colspan=2)

    grid(add_button, 5, 1, colspan=2)

    website_input.focus()
    window.mainloop()