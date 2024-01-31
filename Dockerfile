FROM python:3.11-slim-buster

# Set the working directory to /app
WORKDIR /app


COPY ./requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app/
# Run app.py when the container launches
CMD ["python", "main.py" ]