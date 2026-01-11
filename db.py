"""
SQLite database handler for usage logging.
"""

import sqlite3
import os
from datetime import datetime
from config import DB_PATH


def get_connection():
    """Returns a database connection."""
    # Ensure data directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    """Initializes the database schema."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usage_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER NOT NULL,
            username TEXT,
            action TEXT NOT NULL,
            target_handle TEXT,
            target_category TEXT,
            language TEXT,
            platform TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_telegram_id ON usage_logs(telegram_id)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_timestamp ON usage_logs(timestamp)
    """)

    conn.commit()
    conn.close()


def log_action(
    telegram_id: int,
    action: str,
    username: str = None,
    target_handle: str = None,
    target_category: str = None,
    language: str = None,
    platform: str = None,
):
    """
    Logs a user action.

    Args:
        telegram_id: User's Telegram ID
        action: Action type (start, select_platform, select_category,
                generate, tweet_clicked, regenerate)
        username: Telegram username (optional)
        target_handle: Target's Twitter handle
        target_category: Target category
        language: Output language selected
        platform: Platform (twitter, instagram)
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO usage_logs
        (telegram_id, username, action, target_handle, target_category, language, platform)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (telegram_id, username, action, target_handle, target_category, language, platform),
    )

    conn.commit()
    conn.close()


def get_user_count() -> int:
    """Returns the number of unique users."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(DISTINCT telegram_id) FROM usage_logs")
    result = cursor.fetchone()[0]
    conn.close()
    return result


def get_action_count(action: str = None) -> int:
    """Returns the count of actions, optionally filtered by type."""
    conn = get_connection()
    cursor = conn.cursor()

    if action:
        cursor.execute("SELECT COUNT(*) FROM usage_logs WHERE action = ?", (action,))
    else:
        cursor.execute("SELECT COUNT(*) FROM usage_logs")

    result = cursor.fetchone()[0]
    conn.close()
    return result


def get_recent_logs(limit: int = 50) -> list:
    """Returns recent log entries."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT telegram_id, username, action, target_handle, language, platform, timestamp
        FROM usage_logs
        ORDER BY timestamp DESC
        LIMIT ?
        """,
        (limit,),
    )

    results = cursor.fetchall()
    conn.close()
    return results


def get_stats() -> dict:
    """Returns usage statistics."""
    conn = get_connection()
    cursor = conn.cursor()

    stats = {}

    # Total users
    cursor.execute("SELECT COUNT(DISTINCT telegram_id) FROM usage_logs")
    stats["total_users"] = cursor.fetchone()[0]

    # Total actions
    cursor.execute("SELECT COUNT(*) FROM usage_logs")
    stats["total_actions"] = cursor.fetchone()[0]

    # Actions by type
    cursor.execute(
        """
        SELECT action, COUNT(*) FROM usage_logs
        GROUP BY action ORDER BY COUNT(*) DESC
        """
    )
    stats["actions_by_type"] = dict(cursor.fetchall())

    # Top targets
    cursor.execute(
        """
        SELECT target_handle, COUNT(*) FROM usage_logs
        WHERE target_handle IS NOT NULL
        GROUP BY target_handle ORDER BY COUNT(*) DESC LIMIT 10
        """
    )
    stats["top_targets"] = dict(cursor.fetchall())

    # Languages used
    cursor.execute(
        """
        SELECT language, COUNT(*) FROM usage_logs
        WHERE language IS NOT NULL
        GROUP BY language ORDER BY COUNT(*) DESC
        """
    )
    stats["languages"] = dict(cursor.fetchall())

    # Today's activity
    cursor.execute(
        """
        SELECT COUNT(*) FROM usage_logs
        WHERE date(timestamp) = date('now')
        """
    )
    stats["today_actions"] = cursor.fetchone()[0]

    conn.close()
    return stats
