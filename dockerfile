# Use an official Python image as the base
FROM python:3.12-slim



# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install system dependencies (optional but helpful for some packages like matplotlib)
RUN apt-get update && \
    apt-get install -y build-essential gcc libatlas-base-dev && \
    rm -rf /var/lib/apt/lists/*

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Make port 62255 available to the world outside this container for jupyter
EXPOSE 8888

# Copy the rest of the project files into the container
COPY . .

# Default command (you can modify this based on your project's entry point)
CMD ["python"]

# Run Jupyter Notebook when the container launches
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]