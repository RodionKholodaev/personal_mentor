PRAGMA foreign_keys = ON; -- это делает так что база данных удаляет все записи что ссылаются на удаленный объект

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tg_user_id INTEGER UNIQUE NOT NULL,
    timezone TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_users_tg_user_id ON users(tg_user_id); -- позволяет быстро искать информацию по таблицам


CREATE TABLE IF NOT EXISTS user_profile (
    user_id INTEGER PRIMARY KEY,
    sex TEXT,
    birthdate TEXT,
    height_cm REAL,
    weight_kg REAL,
    activity_level TEXT,
    goal TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    -- тут нужно хранить бжу и каллории
);



CREATE TABLE IF NOT EXISTS user_preferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- полезно для удаления записей и соединения таблиц
    user_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    text TEXT NOT NULL,
    normalized_json TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_user_preferences_user_id ON user_preferences(user_id);

CREATE TABLE IF NOT EXISTS generated_meals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    planned_date TEXT NOT NULL,      -- Дата (ГГГГ-ММ-ДД)
    meal_type TEXT NOT NULL,         -- 'breakfast', 'lunch', 'dinner'
    recipe_json TEXT NOT NULL,       -- Весь ответ нейросети в формате JSON
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS weekly_shopping_lists (
    user_id INTEGER NOT NULL,
    week_start_date TEXT NOT NULL,
    items_json TEXT NOT NULL, -- Тот самый массив из нейросети
    PRIMARY KEY (user_id, week_start_date),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_meals_query ON generated_meals(user_id, planned_date);

------------------------------- эрнест


--CREATE TABLE IF NOT EXISTS notification_templates (
--    id INTEGER PRIMARY KEY AUTOINCREMENT,
--    key TEXT UNIQUE NOT NULL,
--    text TEXT NOT NULL,
--    created_at TEXT NOT NULL
--);


CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    type TEXT NOT NULL,              -- "breakfast", "workout", "water"
    text TEXT NOT NULL,              -- Готовое сообщение
    scheduled_at TEXT NOT NULL,      -- "2026-02-28 08:00:00"
    status TEXT NOT NULL CHECK (status IN ('scheduled', 'sent', 'canceled', 'failed')),
    payload_json TEXT,               -- {"calories": 450, "recipe": "..."}
    created_at TEXT NOT NULL,
    sent_at TEXT,
    error TEXT,                      -- "User blocked bot"
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_status ON notifications(status);    
CREATE INDEX IF NOT EXISTS idx_notifications_scheduled_at ON notifications(scheduled_at);

