import sqlite3
from datetime import datetime


DB_PATH = "database.db"
SCHEMA_PATH = "schema.sql"


def init_db():
    # если файл БД уже есть — SQLite просто подключится
    conn = sqlite3.connect(DB_PATH)

    try:
        conn.execute("PRAGMA foreign_keys = ON;") # говорим что нужно проверять правильность связи между таблицами

        # читаем SQL-схему из файла
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            schema_sql = f.read()

        # выполняем весь SQL одним вызовом
        conn.executescript(schema_sql)

        conn.commit()
        print("Database initialized successfully.")

    finally:
        conn.close()


def save_user_profile(user_id, sex=None, birthdate=None, height_cm=None, weight_kg=None, activity_level=None, goal=None):

    conn = sqlite3.connect("database.db")
    try:
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM user_profile WHERE user_id = ?", (user_id,))
        exists = cursor.fetchone()
        now = datetime.now().isoformat()

        if exists:
            cursor.execute("""
                UPDATE user_profile
                SET sex = COALESCE(?, sex),
                    birthdate = COALESCE(?, birthdate),
                    height_cm = COALESCE(?, height_cm),
                    weight_kg = COALESCE(?, weight_kg),
                    activity_level = COALESCE(?, activity_level),
                    goal = COALESCE(?, goal),
                    updated_at = ?
                WHERE user_id = ?
            """, (sex, birthdate, height_cm, weight_kg, activity_level, goal, now, user_id))
        else:
            cursor.execute("""
                INSERT INTO user_profile (user_id, sex, birthdate, height_cm, weight_kg, activity_level, goal, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_id, sex, birthdate, height_cm, weight_kg, activity_level, goal, now, now))

        conn.commit()
    finally:
        conn.close()
