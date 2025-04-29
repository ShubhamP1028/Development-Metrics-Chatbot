# Use the official Python image from the Docker Hub
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Expose port 5000 to the outside world
EXPOSE 5000

# Set the environment variable to indicate the Flask app
ENV FLASK_APP=app.py

# Run the Flask application
CMD ["python", "app.py"]
