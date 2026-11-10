# Base image: slim Python 3.12
FROM python:3.12-slim
# Working directory for the following instructions and the running app
WORKDIR /app
# Copy requirements first so the install layer is cached until they change
COPY requirements.txt .
# Install dependencies without keeping the pip cache (smaller image)
RUN pip install --no-cache-dir -r requirements.txt
# Application code
COPY app.py .
# Run as an unprivileged user
USER nobody
# Documents the port Flask listens on
EXPOSE 5000
# Start the Flask API
CMD ["python", "app.py"]
