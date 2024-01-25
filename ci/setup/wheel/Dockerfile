FROM python:3.11-slim-buster

# Set the working directory to /app
WORKDIR /app

# RUN apt-get update && apt-get install -y \
#     python3-dev \
#     && rm -rf /var/lib/apt/lists/*
# Copy the current directory contents into the container at /app
COPY ./requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./src /app/src

# Make port 80 available to the world outside this container
EXPOSE 8080

# Run app.py when the container launches
CMD ["python", "src/run.py", "--prod"]