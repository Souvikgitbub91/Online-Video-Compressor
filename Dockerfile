FROM python:3.9-slim

# Install FFmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy app code
COPY . .

# Expose the port (Render will override this)
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
