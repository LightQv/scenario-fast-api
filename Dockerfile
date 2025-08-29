FROM python:3.12-slim

# Environment variables for Python optimization
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create non-root user for security
RUN useradd -ms /bin/sh user -u 1000 \
    && mkdir -p /scenario \
    && chown -R user:user /scenario

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy configuration files
COPY ./requirements.txt /scenario/
COPY ./alembic.ini /scenario/
COPY ./.pylintrc /scenario/

WORKDIR /scenario

# Install uv for faster Python package installation
RUN pip install uv

# Install Python dependencies
RUN uv pip install --system --no-cache-dir -r requirements.txt

# Copy application code
COPY ./app /scenario/app

# Switch to non-root user
USER user

# Expose the application port
EXPOSE 8000

# Run database migrations
CMD ["alembic", "upgrade", "head"]

# Default command for development
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]