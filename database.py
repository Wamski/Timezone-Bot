import sqlite3

def init_db():
    connection = sqlite3.connect('bot_data.db')
    cursor = connection.cursor()

    # Create user preference table 
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS
    user_prefs(user_id INTEGER PRIMARY KEY, timezone TEXT NOT NULL)
    """)

    connection.commit()
    connection.close()

def set_user_timezone(user_id: int, timezone: str) -> None:
    connection = sqlite3.connect('bot_data.db')
    cursor = connection.cursor()

    # Upsert: Insert if new, update if exists
    cursor.execute("""
    INSERT INTO user_prefs(user_id, timezone)
    VALUES (?, ?)
    ON CONFLICT
    DO UPDATE SET timezone = excluded.timezone;
    """, (user_id, timezone))

    connection.commit()
    connection.close()


def get_user_timezone(user_id: int) -> str:
    connection = sqlite3.connect('bot_data.db')
    cursor = connection.cursor()


    # Get the timezone of the user_id
    cursor.execute("""
    SELECT timezone FROM user_prefs WHERE user_id = ?
    """, (user_id,))

    # Fetch the response
    result: str = cursor.fetchone()

    connection.close()

    if result:
        return result[0]
    else:
        return "UTC"


