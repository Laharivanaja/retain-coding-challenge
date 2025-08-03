from models.user_model import get_db_connection

conn = get_db_connection()
cursor = conn.cursor()

def get_all_users():
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

def get_user(user_id):
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

def create_user(name, email, password):
    cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
    conn.commit()

def update_user(user_id, name, email):
    cursor.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, user_id))
    conn.commit()

def delete_user(user_id):
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()

def search_users_by_name(name):
    cursor.execute("SELECT * FROM users WHERE name LIKE ?", (f'%{name}%',))
    return cursor.fetchall()

def login_user(email, password):
    cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    return cursor.fetchone()
