from sqlalchemy import create_engine
from mysql import connector

DB_USER = "root"
DB_PASS = "password"
DB_NAME = "student_db"
DB_HOST = "localhost"

engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}")
