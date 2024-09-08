FROM python:3.10-slim

# Set environment variables
ENV KAFKA_BOOTSTRAP_SERVERS="host.docker.internal:9092"

# Set the working directory in the container
WORKDIR /src

# Copy the requirements file into the container
COPY requirements.txt /src/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /src/

# Expose port 7998 for the FastAPI application
EXPOSE 7998

# Run the FastAPI application, specifying that the main file is inside the "app" folder
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7998"]
