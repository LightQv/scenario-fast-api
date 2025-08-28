# SCENARIO API - FastAPI Version

Bienvenue dans la version FastAPI de l'API Scenario ! Une API moderne pour gérer vos watchlists et suivre votre historique de visionnage de films et séries.

## 🚀 Technologies

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)

## 📋 Fonctionnalités

- ✅ **Authentification complète** : Inscription, connexion, mot de passe oublié
- 🎬 **Gestion des watchlists** : Créer, modifier, supprimer vos listes de films/séries
- 👁️ **Historique de visionnage** : Tracker ce que vous avez regardé
- 📊 **Statistiques** : Analyser vos habitudes de visionnage
- 🔐 **Sécurité** : JWT avec cookies HTTPOnly, hashage bcrypt
- 📧 **Emails** : Système de réinitialisation par email avec fastapi-mail
- 🐳 **Multi-environnements** : Dev, Staging, Production avec Docker
- 🔍 **Monitoring** : Logging avec Loguru, tracking d'erreurs avec Sentry

## 🏗️ Architecture

```
app/
├── core/           # Configuration, database, sécurité
├── models/         # Modèles SQLAlchemy
├── schemas/        # Schémas Pydantic
├── api/v1/         # Routes API
├── services/       # Logique métier
└── utils/          # Utilitaires (templates email, etc.)
```

## 🚀 Démarrage Rapide

### Avec Makefile (Recommandé)

```bash
# Cloner le repository
git clone <votre-repo>
cd scenario-fastapi

# Copier et configurer l'environnement
cp .env.example .env
# Éditer le fichier .env

# Démarrer l'environnement de développement
make dev

# Voir les logs
make dev-logs

# Arrêter l'environnement
make dev-stop
```

### Installation manuelle

1. **Prérequis**
   - Python 3.12+
   - PostgreSQL
   - Docker et Docker Compose

2. **Installation**
```bash
# Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows

# Installer les dépendances
make install
# ou pip install -r requirements.txt

# Configuration
cp .env.example .env
```

3. **Base de données**
```bash
# Avec Docker
make dev

# Ou manuellement
alembic upgrade head
```

## 🐳 Environnements Docker

### Développement
```bash
make dev              # Démarrer
make dev-logs         # Voir les logs  
make dev-stop         # Arrêter
```
- API: http://localhost:8000
- Adminer: http://localhost:8080
- Hot reload activé

### Staging
```bash
make staging          # Démarrer
make staging-stop     # Arrêter
```
- API avec Nginx: http://localhost:8001
- Rate limiting activé
- Sécurité renforcée

### Production
```bash
make prod             # Démarrer
make prod-stop        # Arrêter
```
- HTTPS avec SSL
- Rate limiting agressif
- Monitoring complet

## 📦 Déploiement avec Images Docker

### Build et Push vers DockerHub

```bash
# Configuration du registry
export DOCKER_REGISTRY=your-dockerhub-username

# Build et push
make push

# Ou avec le script de déploiement
chmod +x scripts/deploy.sh
./scripts/deploy.sh --environment prod --registry your-dockerhub-username
```

### Utilisation des images en production

```bash
# Modifier docker-compose.prod.yaml
services:
  scenario-api:
    image: your-dockerhub-username/scenario-api:latest
    # ...
```

## 🔧 Variables d'environnement

### Développement (.env)
```env
APP_NAME="Scenario API"
DEBUG=true
DATABASE_URL="postgresql://scenario_user:scenario_password@localhost:5432/scenario_db"
JWT_SECRET_KEY="your_dev_secret"
FRONTEND_URL="http://localhost:3000"
```

### Production (.env.prod)
```env
APP_NAME="Scenario API"
DEBUG=false
DATABASE_URL="postgresql://prod_user:strong_password@scenario-postgres:5432/scenario_prod_db"
JWT_SECRET_KEY="very_long_and_secure_production_key"
FRONTEND_URL="https://scenario.yourdomain.com"
SENTRY_DSN="https://your-sentry-dsn@sentry.io/project-id"
```

## 📚 Documentation API

- **Swagger UI** : `http://localhost:8000/docs`
- **ReDoc** : `http://localhost:8000/redoc`

## 🛠️ Commandes Utiles

```bash
# Tests
make test             # Lancer les tests
pytest --cov=app     # Tests avec couverture

# Linting
make lint             # Vérifier le code
make lint-fix         # Corriger automatiquement

# Base de données
make migrate          # Appliquer les migrations
make migrate-create   # Créer une nouvelle migration

# Logs
make logs-dev         # Logs développement
make logs-prod        # Logs production

# Debug
make shell            # Shell dans le container
make db-shell         # Shell PostgreSQL
```

## 🔍 Monitoring et Observabilité

### Logs avec Loguru
```python
from loguru import logger

logger.info("User logged in", user_id=user.id)
logger.error("Database connection failed", error=str(e))
```

### Tracking d'erreurs avec Sentry
```python
# Automatique avec l'intégration FastAPI
# Configuré dans app/main.py
```

### Métriques Nginx
- Logs détaillés avec temps de réponse
- Rate limiting par endpoint
- Headers de sécurité

## 🚨 Sécurité

### Headers de sécurité (Nginx)
- `Strict-Transport-Security`
- `X-Frame-Options`
- `X-XSS-Protection`
- `Content-Security-Policy`

### Rate Limiting
- Auth endpoints: 10 req/s
- API générale: 30 req/s (prod), 10 req/s (staging)
- Burst permettant les pics de trafic

### Authentification
- JWT avec cookies HTTPOnly
- Bcrypt pour le hashage des mots de passe
- Tokens de réinitialisation sécurisés
- Validation stricte des entrées avec Pydantic

## 🧪 Tests

```bash
# Lancer tous les tests
make test

# Tests avec couverture détaillée
pytest --cov=app --cov-report=html
open htmlcov/index.html

# Tests en mode watch (développement)
make test-watch

# Tests d'un module spécifique
pytest tests/test_auth.py -v
```

## 📁 Structure des fichiers Docker

```
├── Dockerfile              # Production
├── Dockerfile.dev          # Développement
├── docker-compose.dev.yaml # Environnement dev
├── docker-compose.staging.yaml # Environnement staging  
├── docker-compose.prod.yaml # Environnement production
├── nginx/
│   ├── nginx.dev.conf      # Config Nginx dev
│   ├── nginx.staging.conf  # Config Nginx staging
│   └── nginx.prod.conf     # Config Nginx prod
├── scripts/
│   └── deploy.sh           # Script de déploiement
└── Makefile                # Commandes utiles
```

## 🔄 Workflow de Déploiement

### 1. Développement Local
```bash
# Développer en local avec hot reload
make dev
```

### 2. Tests et Validation
```bash
# Tests unitaires
make test

# Vérification du code
make lint
```

### 3. Déploiement Staging
```bash
# Build et déploiement en staging
./scripts/deploy.sh --environment staging
```

### 4. Déploiement Production
```bash
# Build, push vers DockerHub et déploiement
./scripts/deploy.sh --environment prod --registry your-dockerhub-username
```

## 🌐 Configuration SSL/HTTPS (Production)

### 1. Certificats Let's Encrypt
```bash
# Créer le dossier des certificats
mkdir -p certs

# Obtenir les certificats (avec certbot)
certbot certonly --webroot -w /var/www/certbot -d yourdomain.com
```

### 2. Renouvellement automatique
```bash
# Ajouter au crontab
0 12 * * * /usr/bin/certbot renew --quiet
```

## 📊 Monitoring Avancé

### Health Checks
- Endpoint `/health` pour vérifier l'état de l'API
- Health checks Docker pour les containers
- Monitoring de la base de données

### Métriques personnalisées
```python
# Dans vos endpoints
from loguru import logger
import time

@router.post("/example")
def example_endpoint():
    start_time = time.time()
    # ... logique métier
    duration = time.time() - start_time
    logger.info("Endpoint executed", endpoint="example", duration=duration)
```

## 🔧 Configuration Avancée

### Variables d'environnement par service

#### Base de données
```env
POSTGRES_DB=scenario_db
POSTGRES_USER=scenario_user  
POSTGRES_PASSWORD=secure_password
```

#### Email (Gmail avec mot de passe d'application)
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_specific_password
SMTP_USE_TLS=true
```

#### Sentry (Monitoring d'erreurs)
```env
SENTRY_DSN=https://your_key@sentry.io/project_id
```

## 🚀 Optimisations de Performance

### Base de données
- Indexes sur les colonnes fréquemment requêtées
- Connection pooling avec SQLAlchemy
- Requêtes optimisées avec jointures

### Application
- Réutilisation des connexions HTTP avec `httpx`
- Mise en cache des sessions de base de données
- Validation Pydantic optimisée

### Infrastructure
- Nginx comme reverse proxy
- Gzip compression
- Keep-alive connections
- Buffer optimization

## 🔍 Debugging

### Logs de développement
```bash
# Voir les logs en temps réel
make dev-logs

# Logs d'un service spécifique
docker-compose -f docker-compose.dev.yaml logs -f scenario-api
```

### Accès aux containers
```bash
# Shell dans le container API
make shell

# Shell PostgreSQL
make db-shell

# Inspecter la base de données
docker-compose -f docker-compose.dev.yaml exec scenario-postgres \
  psql -U scenario_user -d scenario_db -c "SELECT * FROM user_model LIMIT 5;"
```

## 📈 Migration depuis Express

### Données existantes
```bash
# Les modèles SQLAlchemy sont compatibles avec votre schéma Express
# Pas besoin de migration de données si vous utilisez la même DB
```

### Changements d'API
- Routes préfixées par `/api/v1/`
- Réponses JSON normalisées
- Validation automatique des entrées
- Documentation automatique

### Frontend
```javascript
// Ancien (Express)
const response = await fetch('/auth/login', { ... })

// Nouveau (FastAPI)  
const response = await fetch('/api/v1/auth/login', { ... })
```

## 🤝 Contribution

### Standards de code
- PEP 8 pour le style Python
- Docstrings pour toutes les fonctions publiques
- Type hints obligatoires
- Tests unitaires pour les nouvelles fonctionnalités

### Workflow
1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/amazing-feature`)
3. Respecter les standards (`make lint`)
4. Ajouter des tests (`make test`)
5. Commit avec des messages clairs
6. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence ISC - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🆘 Support et FAQ

### Problèmes courants

**Port déjà utilisé**
```bash
# Vérifier les ports utilisés
lsof -i :8000

# Ou changer le port dans .env
APP_PORT=8001
```

**Problème de connexion à la DB**
```bash
# Vérifier que PostgreSQL est démarré
make dev-logs

# Recréer les volumes si nécessaire
docker-compose -f docker-compose.dev.yaml down -v
make dev
```

**Erreurs SSL en production**
```bash
# Vérifier les certificats
docker-compose -f docker-compose.prod.yaml exec scenario-nginx \
  openssl x509 -in /etc/nginx/certs/fullchain.pem -text -noout
```

### Ressources utiles
- [Documentation FastAPI](https://fastapi.tiangolo.com/)
- [Documentation SQLAlchemy](https://docs.sqlalchemy.org/)
- [Documentation Pydantic](https://docs.pydantic.dev/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

---

**Développé avec ❤️ en FastAPI par [Votre Nom]**

🔗 **Liens utiles :**
- API Docs: `http://localhost:8000/docs`
- Adminer: `http://localhost:8080` 
- Monitoring: Configurez Sentry pour le monitoring en production