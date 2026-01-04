# Use Python 3.10 base image
FROM python:3.10-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY messaging_app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Django project
COPY messaging_app /app

# Expose Django port
EXPOSE 8000

# Run Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
