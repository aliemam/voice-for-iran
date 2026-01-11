# Voice for Iran - Scripts Documentation

## Database Scripts

These bash scripts help you manage and monitor the bot's SQLite database.

### Setup Database

```bash
./scripts/setup_db.sh
```

Initializes the SQLite database. Run this once before starting the bot for the first time.

- Creates the `data/` directory if it doesn't exist
- Creates `usage.db` with the required tables
- Safe to run multiple times (won't overwrite existing data)

---

### View Logs

```bash
./scripts/view_logs.sh [limit]
```

Shows recent bot activity.

**Arguments:**
- `limit` (optional): Number of entries to show. Default: 50

**Examples:**
```bash
./scripts/view_logs.sh        # Show last 50 entries
./scripts/view_logs.sh 100    # Show last 100 entries
./scripts/view_logs.sh 10     # Show last 10 entries
```

**Output columns:**
- `time` - When the action happened
- `telegram_id` - User's Telegram ID
- `username` - Telegram username (if available)
- `action` - What they did (start, generate, select_platform, etc.)
- `target` - Twitter handle they targeted
- `lang` - Language selected for the message

---

### Statistics

```bash
./scripts/stats.sh
```

Shows usage statistics for the bot.

**Output includes:**
- **Overview**: Total users, total actions, today's actions, tweets generated
- **Actions by Type**: Breakdown of what users are doing
- **Top 10 Targets**: Most targeted Twitter accounts
- **Languages Used**: Which output languages are popular
- **Activity by Day**: Last 7 days of activity

---

## Quick Reference

```bash
# On Raspberry Pi
ssh rasp
cd ~/voice_for_iran

# View recent activity
./scripts/view_logs.sh

# See full statistics
./scripts/stats.sh

# Check if database exists
ls -la data/usage.db
```

## Docker Usage

When running with Docker, the database is stored in `./data/usage.db` on the host machine (mounted volume). Scripts work the same way.

```bash
# Check logs while bot is running in Docker
./scripts/view_logs.sh

# Get stats
./scripts/stats.sh
```

## Database Location

- **Path**: `data/usage.db`
- **Type**: SQLite 3
- **Tables**: `usage_logs`

## Direct Database Access

If you need to run custom queries:

```bash
sqlite3 data/usage.db

# Example queries inside sqlite3:
SELECT * FROM usage_logs ORDER BY timestamp DESC LIMIT 10;
SELECT COUNT(*) FROM usage_logs WHERE action = 'generate';
.quit
```
