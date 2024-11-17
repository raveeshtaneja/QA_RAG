FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Make start.sh executable
RUN chmod +x start.sh

# Expose ports for Flask and Streamlit
EXPOSE 5000 8501

# Run start.sh when container starts
CMD ["./start.sh"] 