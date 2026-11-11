import aiosqlite
import datetime

DB_PATH = "users.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_seen DATE,
                folders_count INTEGER DEFAULT 0
            )
        """)
        await db.commit()

async def add_user(user_id: int, username: str) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,)) as cursor:
            if await cursor.fetchone():
                return False  # Юзер уже есть
        
        today = datetime.date.today().isoformat()
        await db.execute(
            "INSERT INTO users (user_id, username, first_seen) VALUES (?, ?, ?)",
            (user_id, username, today)
        )
        await db.commit()
        return True  # Юзер новый

async def increment_folders(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET folders_count = folders_count + 1 WHERE user_id = ?",
            (user_id,)
        )
        await db.commit()

async def get_stats() -> dict:
    async with aiosqlite.connect(DB_PATH) as db:
        # Всего юзеров
        async with db.execute("SELECT COUNT(*) FROM users") as cursor:
            total_users = (await cursor.fetchone())[0]
        
        # Новых за сегодня
        today = datetime.date.today().isoformat()
        async with db.execute("SELECT COUNT(*) FROM users WHERE first_seen = ?", (today,)) as cursor:
            new_today = (await cursor.fetchone())[0]
            
        # Всего папок
        async with db.execute("SELECT SUM(folders_count) FROM users") as cursor:
            total_folders = (await cursor.fetchone())[0] or 0
            
        return {
            "total_users": total_users,
            "new_today": new_today,
            "total_folders": total_folders
        }