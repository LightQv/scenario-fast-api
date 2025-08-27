FROM python:3.12-slim

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Créer un utilisateur non-root
RUN useradd -ms /bin/sh user -u 1000 \
    && mkdir -p /scenario \
    && chown -R user:user /scenario

# Installer les dépendances système
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers de configuration
COPY ./requirements.txt /scenario/
COPY ./alembic.ini /scenario/
COPY ./.pylintrc /scenario/

WORKDIR /scenario

# Installer uv pour une installation plus rapide
RUN pip install uv

# Installer les dépendances Python
RUN uv pip install --system --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY ./app /scenario/app

# Changer vers l'utilisateur non-root
USER user

# Exposer le port
EXPOSE 8000

CMD ["alembic", "upgrade", "head"]

# Commande par défaut pour le développement
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]