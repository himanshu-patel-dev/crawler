# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (for psycopg2, lxml, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    curl \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install pip requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Copy entrypoint
COPY entrypoint.sh /entrypoint.sh
# Make it executable
RUN chmod +x /entrypoint.sh

# Collect static files (for prod)
RUN python manage.py collectstatic --noinput

# Expose Django port
EXPOSE 8000

# Default command (overridden in docker-compose)
CMD ["gunicorn", "crawler_service.wsgi:application", "--bind", "0.0.0.0:8000", "--workers=3"]
