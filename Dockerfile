FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY bot.py .
COPY ai_generator.py .
COPY config.py .
COPY db.py .
COPY targets.py .
COPY templates.py .

# Create data directory for SQLite
RUN mkdir -p /app/data

# Run the bot
CMD ["python", "bot.py"]
