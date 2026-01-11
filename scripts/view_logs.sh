#!/bin/bash
# View recent usage logs for Voice for Iran bot

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
DB_PATH="$PROJECT_DIR/data/usage.db"

# Default limit
LIMIT=${1:-50}

if [ ! -f "$DB_PATH" ]; then
    echo "Database not found. Run setup_db.sh first."
    exit 1
fi

echo "=== Recent Activity (last $LIMIT entries) ==="
echo ""

sqlite3 -header -column "$DB_PATH" <<EOF
SELECT
    datetime(timestamp, 'localtime') as time,
    telegram_id,
    COALESCE(username, '-') as username,
    action,
    COALESCE(target_handle, '-') as target,
    COALESCE(language, '-') as lang
FROM usage_logs
ORDER BY timestamp DESC
LIMIT $LIMIT;
EOF
