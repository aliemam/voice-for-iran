#!/bin/bash
# Initialize the SQLite database for Voice for Iran bot

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
DB_PATH="$PROJECT_DIR/data/usage.db"

echo "Setting up Voice for Iran database..."

# Create data directory if it doesn't exist
mkdir -p "$PROJECT_DIR/data"

# Create the database and tables
sqlite3 "$DB_PATH" <<EOF
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
);

CREATE INDEX IF NOT EXISTS idx_telegram_id ON usage_logs(telegram_id);
CREATE INDEX IF NOT EXISTS idx_timestamp ON usage_logs(timestamp);
EOF

if [ $? -eq 0 ]; then
    echo "Database created successfully at: $DB_PATH"
else
    echo "Error creating database!"
    exit 1
fi
