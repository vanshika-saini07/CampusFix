import os
import mysql.connector
from werkzeug.security import generate_password_hash

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", ""),
    database=os.getenv("DB_NAME", "campusfix"),
    port=int(os.getenv("DB_PORT", "3306"))
)

cursor = conn.cursor()

name = input("Enter admin name: ")
email = input("Enter admin email: ").strip().lower()
password = input("Create admin password: ")

hashed_password = generate_password_hash(password)

cursor.execute(
    """
    INSERT INTO admins (name, email, password)
    VALUES (%s, %s, %s)
    """,
    (name, email, hashed_password)
)

conn.commit()

print("Admin account created successfully!")

cursor.close()
conn.close()