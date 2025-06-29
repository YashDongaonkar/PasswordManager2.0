# 🔐 Secure Password Manager

A secure, multi-user password manager built with **Python**, featuring:

* 🔑 **User authentication** with `bcrypt`-hashed master passwords
* 🧠 **AES-encrypted password vaults** (unique encryption per user)
* ☁️ **MongoDB Atlas** backend for persistent, isolated user data
* 🖥️ **Tkinter GUI** for a simple and intuitive desktop experience

---

## ✨ Features

* **User Registration & Login**

  * Secure signup with `bcrypt` password hashing
  * Unique user-based vault isolation
* **Encrypted Vault**

  * Vault entries encrypted using `AES` with user-derived keys
  * Secure tokenization and de-tokenization
* **Password Storage**

  * Store website, username, and password entries
  * Edit , search and create entries through GUI

* **Backend**

  * MongoDB Atlas handles persistent storage per user

---

## 🛡️ Security Highlights

* Passwords **never stored in plain text**
* Vault entries are **AES-encrypted with a key derived from the user password**
* All operations are **scoped per-user** to ensure data isolation
---

## 🧩 Dependencies

* `pymongo`
* `bcrypt`
* `cryptography`
* `tkinter` (built-in for Python)
* `base64`, `hashlib`, `os`, `json`
