# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
# Note: This copies the adk_agent folder into the container
COPY adk_agent/ ./adk_agent/

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Expose the port the ADK server runs on
EXPOSE 8080

# Set the working directory to where the agent is defined
WORKDIR /app/adk_agent

# Run the agent using the ADK web server
CMD ["adk", "web", "--port", "8080", "--host", "0.0.0.0"]
