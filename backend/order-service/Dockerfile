FROM python:3.9

# Set environment variables
ENV KAFKA_BOOTSTRAP_SERVERS="host.docker.internal:9092"

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file into the container
COPY ./requirements.txt /code/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of the application code into the container
COPY ./app /code/app

# Expose port 7998 for the FastAPI application
EXPOSE 8000

# Run the FastAPI application, specifying that the main file is inside the "app" folder
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
