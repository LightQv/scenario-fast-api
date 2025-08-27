# SCENARIO API - FastAPI Version

Bienvenue dans la version FastAPI de l'API Scenario ! Une API moderne pour gérer vos watchlists et suivre votre historique de visionnage de films et séries.

## 🚀 Technologies

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Pytest](https://img.shields.io/badge/pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)

## 📋 Fonctionnalités

- ✅ **Authentification complète** : Inscription, connexion, mot de passe oublié
- 🎬 **Gestion des watchlists** : Créer, modifier, supprimer vos listes de films/séries
- 👁️ **Historique de visionnage** : Tracker ce que vous avez regardé
- 📊 **Statistiques** : Analyser vos habitudes de visionnage
- 🔐 **Sécurité** : JWT avec cookies HTTPOnly, hashage Argon2
- 📧 **Emails** : Système de réinitialisation par email

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

## 🚀 Installation et Démarrage

### Prérequis

- Python 3.11+
- PostgreSQL
- Docker et Docker Compose (optionnel)

### Installation classique

1. **Cloner le repository**
```bash
git clone <votre-repo>
cd scenario-fastapi
```

2. **Créer l'environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configuration**
```bash
cp .env.example .env
# Éditer le fichier .env avec vos configurations
```

5. **Base de données**
```bash
# Initialiser Alembic
alembic init alembic

# Créer la migration initiale
alembic revision --autogenerate -m "Initial migration"

# Appliquer les migrations
alembic upgrade head
```

6. **Lancer l'API**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Installation avec Docker

1. **Lancer avec Docker Compose**
```bash
docker-compose up -d
```

2. **Appliquer les migrations**
```bash
docker-compose exec api alembic upgrade head
```

L'API sera disponible sur `http://localhost:8000`

## 📚 Documentation API

- **Swagger UI** : `http://localhost:8000/docs`
- **ReDoc** : `http://localhost:8000/redoc`

## 🛠️ Endpoints principaux

### Authentification
- `POST /api/v1/auth/register` - Inscription
- `POST /api/v1/auth/login` - Connexion
- `GET /api/v1/auth/logout` - Déconnexion
- `POST /api/v1/auth/forgotten-password` - Mot de passe oublié
- `POST /api/v1/auth/reset-password` - Réinitialiser le mot de passe

### Utilisateurs
- `GET /api/v1/users/{user_id}` - Informations utilisateur
- `PUT /api/v1/users/{user_id}` - Modifier utilisateur
- `DELETE /api/v1/users/{user_id}` - Supprimer utilisateur

### Watchlists
- `GET /api/v1/watchlists/{user_id}` - Lister les watchlists
- `GET /api/v1/watchlists/detail/{watchlist_id}` - Détails d'une watchlist
- `POST /api/v1/watchlists` - Créer une watchlist
- `PUT /api/v1/watchlists/{watchlist_id}` - Modifier une watchlist
- `DELETE /api/v1/watchlists/{watchlist_id}` - Supprimer une watchlist

### Médias
- `POST /api/v1/medias` - Ajouter un média à une watchlist
- `PUT /api/v1/medias/{media_id}` - Modifier un média
- `DELETE /api/v1/medias/{media_id}` - Supprimer un média

### Vues (Historique)
- `GET /api/v1/views/{user_id}` - Historique complet
- `GET /api/v1/views/{media_type}/{user_id}` - Historique par type
- `POST /api/v1/views` - Ajouter une vue
- `DELETE /api/v1/views/{view_id}` - Supprimer une vue

### Statistiques
- `GET /api/v1/stats/count/{media_type}/{user_id}` - Nombre par type
- `GET /api/v1/stats/year/{media_type}/{user_id}` - Répartition par année
- `GET /api/v1/stats/runtime/{media_type}/{user_id}` - Durées de visionnage

## 🧪 Tests

```bash
# Lancer tous les tests
pytest

# Tests avec couverture
pytest --cov=app

# Tests spécifiques
pytest tests/test_auth.py
```

## 🔧 Variables d'environnement

Copiez `.env.example` vers `.env` et configurez :

```env
# App Configuration
APP_NAME="Scenario API"
APP_PORT=8000
DEBUG=true

# Database
DATABASE_URL="postgresql://user:password@localhost:5432/scenario_db"

# JWT
JWT_SECRET_KEY="votre_clé_secrète_super_sécurisée"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=43200

# SMTP pour les emails
SMTP_HOST="smtp.gmail.com"
SMTP_USER="votre_email@gmail.com"
SMTP_PASSWORD="votre_mot_de_passe_app"

# Frontend
FRONTEND_URL="http://localhost:3000"
```

## 🐳 Docker

Le projet inclut un `docker-compose.yml` avec :
- **API FastAPI** sur le port 8000
- **PostgreSQL** sur le port 5432
- **Adminer** sur le port 8080 (interface web pour la DB)

```bash
# Démarrer les services
docker-compose up -d

# Voir les logs
docker-compose logs -f api

# Arrêter les services
docker-compose down
```

## 📝 Migration depuis Express

Si vous migrez depuis votre API Express existante :

1. **Données** : Utilisez les mêmes tables PostgreSQL
2. **Authentification** : Les tokens JWT restent compatibles
3. **Frontend** : Adaptez les appels API (structure similaire)

### Différences principales :
- Routes préfixées par `/api/v1/`
- Réponses JSON standardisées
- Validation automatique avec Pydantic
- Documentation automatique

## 🔮 Intégration Plex

Avec FastAPI, l'intégration Plex sera facilitée :

```python
# Exemple futur
from plexapi.server import PlexServer

@router.get("/plex/libraries")
def get_plex_libraries():
    plex = PlexServer('http://localhost:32400', token)
    return plex.library.sections()
```

## 📱 App Mobile React Native

Votre app React Native fonctionnera parfaitement avec cette API :

1. **Même authentification** : JWT dans cookies
2. **Endpoints compatibles** : Structure similaire à Express
3. **Documentation** : Swagger pour référence

## 🤝 Contribution

1. Fork le projet
2. Créez votre branche (`git checkout -b feature/amazing-feature`)
3. Commit vos changements (`git commit -m 'Add amazing feature'`)
4. Push vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est sous licence ISC.

## 🙋‍♂️ Support

Pour toute question ou problème :
- Ouvrez une issue sur GitHub
- Consultez la documentation Swagger à `/docs`

---

**Développé avec ❤️ en FastAPI**