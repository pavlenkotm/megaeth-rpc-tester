# Multi-stage build for efficient image size
FROM python:3.11-slim as builder

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# Final stage
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY rpc_tester/ ./rpc_tester/
COPY setup.py .
COPY README.md .
COPY example_config.yaml .

# Make sure scripts are in PATH
ENV PATH=/root/.local/bin:$PATH

# Create results directory
RUN mkdir -p /app/results

# Set Python to unbuffered mode
ENV PYTHONUNBUFFERED=1

# Default command
ENTRYPOINT ["python", "-m", "rpc_tester"]

# Default arguments (can be overridden)
CMD ["--help"]
