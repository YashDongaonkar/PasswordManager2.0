import bcrypt
from db_utils import users_col

def register_user(username: str, master_password: str) -> bool:

    if users_col.find_one({"_id": username}):
        return (False, "User already exists.")

    hashed_pw = bcrypt.hashpw(master_password.encode(), bcrypt.gensalt())

    users_col.insert_one({
        "_id": username,
        "master_hash": hashed_pw
    })

    return (True, "Registration successful.")

def authenticate_user(username: str, master_password: str) -> bool:
    
    user = users_col.find_one({"_id": username})

    if not user:
        return (False, "User not found.")

    hashed_pw = user["master_hash"]

    if bcrypt.checkpw(master_password.encode(), hashed_pw):
        return (True, "Login successful.")

    return (False, "Incorrect password.")
