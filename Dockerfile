FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for AutoGluon
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and model
COPY src/app.py ./src/
COPY models/autogluon_model ./models/autogluon_model

# Expose port
EXPOSE 8000

# Set Python unbuffered for logging
ENV PYTHONUNBUFFERED=1

# Run FastAPI
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
