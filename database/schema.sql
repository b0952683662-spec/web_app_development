-- ============================================================
-- schema.sql — 食譜收藏夾系統 資料庫建表語法
-- 使用：SQLite
-- ============================================================

-- 使用者資料表
CREATE TABLE IF NOT EXISTS users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT    NOT NULL UNIQUE,
    email         TEXT    NOT NULL UNIQUE,
    password_hash TEXT    NOT NULL,
    role          TEXT    NOT NULL DEFAULT 'user',  -- 'user' or 'admin'
    created_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 食譜資料表
CREATE TABLE IF NOT EXISTS recipes (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT    NOT NULL,
    description TEXT,
    difficulty  INTEGER NOT NULL CHECK(difficulty BETWEEN 1 AND 5),
    cook_time   INTEGER,                          -- 單位：分鐘
    image_path  TEXT,                             -- 相對於 static/uploads/
    user_id     INTEGER NOT NULL,
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 食材資料表
CREATE TABLE IF NOT EXISTS ingredients (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    name      TEXT    NOT NULL,
    amount    TEXT,                               -- 份量（如：2顆、100g）
    recipe_id INTEGER NOT NULL,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
);

-- 烹飪步驟資料表
CREATE TABLE IF NOT EXISTS steps (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    order_num INTEGER NOT NULL,                   -- 步驟順序，從 1 開始
    content   TEXT    NOT NULL,
    recipe_id INTEGER NOT NULL,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
);

-- 分類標籤資料表
CREATE TABLE IF NOT EXISTS categories (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- 食譜分類關聯表（多對多）
CREATE TABLE IF NOT EXISTS recipe_category (
    recipe_id   INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    PRIMARY KEY (recipe_id, category_id),
    FOREIGN KEY (recipe_id)   REFERENCES recipes(id)    ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);

-- ============================================================
-- 初始資料：預設分類標籤
-- ============================================================
INSERT OR IGNORE INTO categories (name) VALUES
    ('早餐'),
    ('午餐'),
    ('晚餐'),
    ('甜點'),
    ('素食'),
    ('湯品'),
    ('點心'),
    ('義式料理'),
    ('日式料理'),
    ('中式料理');
