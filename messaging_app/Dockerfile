# Use Python 3.10 base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y build-essential && apt-get clean

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy full Django project
COPY . /app/

# Expose Django default port
EXPOSE 8000

# Default command to run the server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
