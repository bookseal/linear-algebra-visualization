FROM manimcommunity/manim:latest

# Switch to root to install dependencies
USER root

# Install system dependencies if any (manim image is quite complete, but we might need some for streamlit)
# Running apt-get update just in case
RUN apt-get update && apt-get install -y \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create app directory and set permissions
WORKDIR /app
RUN chown -R manimuser:manimuser /app

# Switch back to manimuser
USER manimuser

# Expose Streamlit port
EXPOSE 8501

# Healthcheck for Streamlit
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Default command
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
