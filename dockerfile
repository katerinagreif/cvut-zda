# Use an official Python image as the base
FROM python:latest


# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the project files into the container
COPY . .

# Default command (you can modify this based on your project's entry point)
CMD ["python"]
