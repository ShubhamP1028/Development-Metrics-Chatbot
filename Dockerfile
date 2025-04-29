# Use official Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies (for MySQL support)
RUN apt-get update && apt-get install -y default-libmysqlclient-dev gcc

# Copy all project files into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir Flask mysql-connector-python

# Expose the Flask default port
EXPOSE 5000

# Command to run your app
CMD ["python", "app.py"]
