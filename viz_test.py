import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="NewPassword",
        database="student_db"
    )
    print("✅ MySQL Connection Successful!")
    conn.close()
except Exception as e:
    print(f"❌ MySQL Connection Failed: {e}")
