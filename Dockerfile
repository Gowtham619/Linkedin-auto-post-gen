FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY src/ ./src/
COPY config/ ./config/

# Create directories
RUN mkdir -p content logs

# Create non-root user
RUN useradd -m -u 1000 agent && chown -R agent:agent /app
USER agent

# Environment
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30m --timeout=10s --start-period=1m \
  CMD python -c "import os; exit(0 if os.path.exists('/app/logs/agent.log') else 1)"

# Run the agent
CMD ["python", "src/content_agent.py"]
