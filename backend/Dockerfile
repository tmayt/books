# Use Python slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       gcc \
       libpq-dev \
       libc-dev \
       build-essential \ 
       postgresql-client \
       graphviz \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/

# Set working directory
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Ensure the entrypoint script is executable
RUN chmod +x /app/entrypoint.sh

# Expose the port for the Django app (change if needed)
EXPOSE 8000

# Set the entrypoint to run the custom entrypoint.sh script
ENTRYPOINT ["/app/entrypoint.sh"]
