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



def register_user_if_not_exists(tg_user_id: int, timezone: str = "UTC"):
    """
    Создает запись в таблице users, если tg_user_id еще не зарегистрирован.
    """
    conn = sqlite3.connect(DB_PATH)
    try:
        now = datetime.now().isoformat()
        # INSERT OR IGNORE предотвратит ошибку, если пользователь уже нажимал /start ранее
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO users (tg_user_id, timezone, created_at)
            VALUES (?, ?, ?)
        """, (tg_user_id, timezone, now))
        conn.commit()
    finally:
        conn.close()


def get_user_id_by_tgid(tg_user_id):
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM users WHERE tg_user_id = ?", (tg_user_id,))
        row = cursor.fetchone()
        if not row:
            raise Exception("нет пользователя с таким tg_user_id")
        
        user_id = row[0]

        return user_id
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


def get_user_profile(tg_user_id: int)-> dict | None:

    conn = sqlite3.connect('database.db')
    
    # Настраиваем row_factory, чтобы получать данные в виде словаря, а не кортежа
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        # Пишем запрос с JOIN
        # Мы объединяем таблицы users и user_profile по внутреннему id
        query = """
        SELECT 
            u.id,
            u.tg_user_id,
            u.timezone,
            p.sex,
            p.birthdate,
            p.height_cm,
            p.weight_kg,
            p.activity_level,
            p.goal
        FROM users u
        JOIN user_profile p ON u.id = p.user_id -- соединили таблицы по u.id = p.user_id
        WHERE u.tg_user_id = ? -- указали tg_user_id
        """
        
        cursor.execute(query, (tg_user_id,))
        result = cursor.fetchone()

        if result:
            # Превращаем результат в обычный словарь Python
            return dict(result)
        else:
            return None # Если пользователь не найден или профиль не заполнен

    except sqlite3.Error as e:
        print(f"Ошибка при работе с базой данных: {e}")
        return None
    finally:
        # Всегда закрываем соединение
        conn.close()
    

