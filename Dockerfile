FROM python:3.12-slim AS builder

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Installer les dépendances de build
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copier requirements et installer les dépendances
COPY requirements.txt .
RUN pip install uv \
    && uv pip install --system --no-cache-dir -r requirements.txt

# Stage final
FROM python:3.12-slim

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Créer un utilisateur non-root
RUN useradd -ms /bin/sh user -u 1000 \
    && mkdir -p /scenario \
    && chown -R user:user /scenario

# Installer uniquement les dépendances runtime
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpq5 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copier les dépendances Python depuis le builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copier les fichiers de l'application
COPY --chown=user:user ./app /scenario/app
COPY --chown=user:user ./alembic.ini /scenario/

WORKDIR /scenario

# Changer vers l'utilisateur non-root
USER user

# Exposer le port
EXPOSE 8000

# Commande de santé
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["alembic", "upgrade", "head"]

# Commande par défaut
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]