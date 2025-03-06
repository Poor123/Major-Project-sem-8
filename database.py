from sqlalchemy import create_engine
DB_USER = "root"
DB_PASS = "NewPassword"  # Ensure this matches the new password
DB_NAME = "student_db"
DB_HOST = "localhost"

engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}")

try:
    with engine.connect() as conn:
        print("✅ Database connection successful!")
except Exception as e:
    print("❌ Error:", e)
