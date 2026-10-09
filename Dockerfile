FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Streamlit port
EXPOSE 8501

# Start the application
CMD ["streamlit", "run", "main.py", "--server.address=0.0.0.0", "--server.port=8501"]
