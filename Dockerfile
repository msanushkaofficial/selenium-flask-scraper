FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget gnupg unzip curl \
    chromium chromium-driver

# Set environment variable for Chromium
ENV CHROME_BIN=/usr/bin/chromium
ENV PATH="$PATH:/usr/lib/chromium/"

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Run app
CMD ["python", "app.py"]
