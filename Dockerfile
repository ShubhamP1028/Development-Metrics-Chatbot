# Use an official Python runtime
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy all project files into the container
COPY . .

# Expose the port your Flask app will run on
EXPOSE 5000

# Run your main application
CMD ["python", "App.py"]

