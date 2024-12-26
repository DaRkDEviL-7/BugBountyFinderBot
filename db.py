import sqlite3
from contextlib import contextmanager

@contextmanager
def get_db_connection():
    conn = sqlite3.connect('bot_data.db')
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS user_points (
                     user_id INTEGER PRIMARY KEY,
                     points INTEGER DEFAULT 0)''')
        c.execute('''CREATE TABLE IF NOT EXISTS user_prefs (
                     user_id INTEGER PRIMARY KEY,
                     keyword TEXT,
                     frequency INTEGER DEFAULT 60)''')
        conn.commit()

def update_points(user_id, points):
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO user_points (user_id, points) VALUES (?, 0)", (user_id,))
        c.execute("UPDATE user_points SET points = points + ? WHERE user_id = ?", (points, user_id))
        conn.commit()

def get_leaderboard():
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT user_id, points FROM user_points ORDER BY points DESC LIMIT 10")
        leaderboard = c.fetchall()
        return leaderboard

def set_user_pref(user_id, keyword, frequency):
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO user_prefs (user_id, keyword, frequency) VALUES (?, ?, ?)",
                  (user_id, keyword, frequency))
        conn.commit()

def get_user_pref(user_id):
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT keyword, frequency FROM user_prefs WHERE user_id = ?", (user_id,))
        pref = c.fetchone()
        return pref
