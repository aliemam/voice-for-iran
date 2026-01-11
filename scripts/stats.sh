#!/bin/bash
# Show usage statistics for Voice for Iran bot

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
DB_PATH="$PROJECT_DIR/data/usage.db"

if [ ! -f "$DB_PATH" ]; then
    echo "Database not found. Run setup_db.sh first."
    exit 1
fi

echo "=========================================="
echo "   Voice for Iran - Usage Statistics"
echo "=========================================="
echo ""

echo "--- Overview ---"
sqlite3 "$DB_PATH" <<EOF
SELECT
    'Total Users' as metric,
    COUNT(DISTINCT telegram_id) as value
FROM usage_logs
UNION ALL
SELECT
    'Total Actions',
    COUNT(*)
FROM usage_logs
UNION ALL
SELECT
    'Today''s Actions',
    COUNT(*)
FROM usage_logs WHERE date(timestamp) = date('now')
UNION ALL
SELECT
    'Tweets Generated',
    COUNT(*)
FROM usage_logs WHERE action = 'generate';
EOF

echo ""
echo "--- Actions by Type ---"
sqlite3 -header -column "$DB_PATH" <<EOF
SELECT action, COUNT(*) as count
FROM usage_logs
GROUP BY action
ORDER BY count DESC;
EOF

echo ""
echo "--- Top 10 Targets ---"
sqlite3 -header -column "$DB_PATH" <<EOF
SELECT target_handle, COUNT(*) as count
FROM usage_logs
WHERE target_handle IS NOT NULL
GROUP BY target_handle
ORDER BY count DESC
LIMIT 10;
EOF

echo ""
echo "--- Languages Used ---"
sqlite3 -header -column "$DB_PATH" <<EOF
SELECT language, COUNT(*) as count
FROM usage_logs
WHERE language IS NOT NULL
GROUP BY language
ORDER BY count DESC;
EOF

echo ""
echo "--- Activity by Day (last 7 days) ---"
sqlite3 -header -column "$DB_PATH" <<EOF
SELECT
    date(timestamp) as day,
    COUNT(*) as actions,
    COUNT(DISTINCT telegram_id) as users
FROM usage_logs
WHERE timestamp >= date('now', '-7 days')
GROUP BY date(timestamp)
ORDER BY day DESC;
EOF

echo ""
echo "=========================================="
