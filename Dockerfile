# Use an official Python runtime as the base image
FROM python:3.9


# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory to the container
COPY . .

# Expose the port the Django app runs on
EXPOSE 8000

# Define the command to start the Django development server
CMD python admin/manage.py runserver 0.0.0.0:8000
