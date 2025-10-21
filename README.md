# News-Paper

Application web de recommandation d'articles scientifiques et de blog personnalisée.

## Description

News-Paper est une plateforme qui explore le web pour collecter des articles issus de publications scientifiques, de revues et de blogs, puis propose du contenu personnalisé basé sur les centres d'intérêt de chaque utilisateur. Les utilisateurs peuvent configurer leurs préférences de notification par email (quotidienne, hebdomadaire, etc.).

## Architecture

### Frontend
- **React** - Framework UI
- **Tailwind CSS** - Styling
- **shadcn/ui** - Composants UI
- **Design responsive** - Compatible mobile, tablette et desktop

### Backend
- **Django** - Framework web
- **Django REST Framework** - API REST
- **Celery** - Tâches asynchrones (scraping, envoi d'emails)
- **PostgreSQL** - Base de données (recommandé en production)

## Fonctionnalités principales

- Inscription et authentification des utilisateurs
- Configuration des centres d'intérêt
- Exploration automatique du web pour collecter des articles
- Système de recommandation personnalisé
- Planification d'envoi d'emails configurables
- Interface responsive (mobile, tablette, desktop)

## Structure du projet

```
News-Paper/
├── backend/          # Application Django
│   ├── api/          # API REST
│   ├── core/         # Modèles et logique métier
│   ├── scraper/      # Module de web scraping
│   └── manage.py
├── frontend/         # Application React
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   └── package.json
└── README.md
```

## Installation

### Backend (Django)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend (React)

```bash
cd frontend
npm install
npm run dev
```

## Développement

Le projet est en cours de développement actif.

## Licence

À définir