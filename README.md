# News Paper

Une application web de découverte et de curation d'articles personnalisés avec des notifications par email.

## Fonctionnalités

- **Authentification utilisateur** : Inscription et connexion sécurisées avec JWT
- **Découverte d'articles** : Exploration automatique d'articles depuis diverses sources (RSS, sites web, blogs, publications scientifiques)
- **Personnalisation** : Sélection de centres d'intérêt pour recevoir des articles pertinents
- **Interactions** : Sauvegarde, j'aime et lecture d'articles
- **Notifications par email** : Réception de digests personnalisés avec plusieurs fréquences disponibles
  - Tous les jours
  - Une fois par semaine
  - Deux fois par semaine
  - Trois fois par semaine
- **Interface responsive** : Optimisée pour mobile, tablette et desktop

## Technologies

### Backend
- **Django 4.2** : Framework web Python
- **Django REST Framework** : API REST
- **JWT Authentication** : Authentification sécurisée
- **Celery** : Tâches asynchrones et planifiées
- **Redis** : Broker pour Celery
- **BeautifulSoup & Feedparser** : Web scraping et parsing RSS
- **SQLite** : Base de données (configurable pour PostgreSQL)

### Frontend
- **React 18** : Bibliothèque UI
- **Vite** : Build tool moderne et rapide
- **Tailwind CSS** : Framework CSS utility-first
- **shadcn/ui** : Composants UI élégants et accessibles
- **React Router** : Navigation côté client
- **Axios** : Client HTTP

## Installation

### Prérequis

- Python 3.11+
- Node.js 18+
- Redis (pour Celery)
- Docker & Docker Compose (optionnel)

### Option 1 : Installation avec Docker (Recommandé)

1. Clonez le repository :
```bash
git clone <repository-url>
cd News-Paper
```

2. Lancez l'application avec Docker Compose :
```bash
docker-compose up --build
```

3. L'application sera accessible à :
   - Frontend : http://localhost
   - Backend API : http://localhost:8000
   - Admin Django : http://localhost:8000/admin

### Option 2 : Installation manuelle

#### Backend

1. Créez un environnement virtuel Python :
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. Créez un fichier `.env` (copiez depuis `.env.example`) :
```bash
cp .env.example .env
```

4. Configurez les variables d'environnement dans `.env`

5. Appliquez les migrations :
```bash
python manage.py migrate
```

6. Créez un superutilisateur :
```bash
python manage.py createsuperuser
```

7. Lancez le serveur :
```bash
python manage.py runserver
```

8. Dans un nouveau terminal, lancez Redis :
```bash
redis-server
```

9. Dans un autre terminal, lancez Celery worker :
```bash
cd backend
celery -A config worker -l info
```

10. Dans un dernier terminal, lancez Celery beat :
```bash
cd backend
celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

#### Frontend

1. Installez les dépendances :
```bash
cd frontend
npm install
```

2. Lancez le serveur de développement :
```bash
npm run dev
```

3. Accédez à l'application : http://localhost:5173

## Configuration

### Ajouter des sources d'articles

1. Connectez-vous à l'admin Django : http://localhost:8000/admin
2. Allez dans "Sources"
3. Ajoutez une nouvelle source avec :
   - Nom de la source
   - URL (RSS feed ou page web)
   - Type de source (RSS, Web, Blog, Scientific)
   - Centres d'intérêt associés
   - État actif

### Ajouter des centres d'intérêt

1. Dans l'admin Django, allez dans "Interests"
2. Ajoutez des centres d'intérêt (ex: Technologie, Science, Sport, etc.)
3. Les utilisateurs pourront les sélectionner dans leurs paramètres

### Configuration des emails

Pour activer l'envoi d'emails, configurez ces variables dans `.env` :

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=votre-email@gmail.com
EMAIL_HOST_PASSWORD=votre-mot-de-passe-app
DEFAULT_FROM_EMAIL=noreply@newspaper.com
```

**Note** : Pour Gmail, vous devez créer un "App Password" dans les paramètres de sécurité de votre compte.

## Utilisation

### Pour les utilisateurs

1. **Inscription** :
   - Créez un compte avec votre email
   - Remplissez vos informations personnelles

2. **Configuration des préférences** :
   - Accédez aux paramètres
   - Sélectionnez vos centres d'intérêt
   - Configurez la fréquence des emails

3. **Navigation** :
   - Consultez les articles sur le tableau de bord
   - Recherchez des articles par mots-clés
   - Sauvegardez vos articles préférés
   - Aimez les articles qui vous intéressent

4. **Réception d'emails** :
   - Recevez des digests personnalisés selon la fréquence choisie
   - Chaque email contient jusqu'à 10 articles correspondant à vos intérêts

### Pour les administrateurs

1. **Gestion des sources** :
   - Ajoutez des sources RSS ou des sites web
   - Associez des centres d'intérêt aux sources
   - Activez/désactivez les sources

2. **Gestion des articles** :
   - Les articles sont automatiquement récupérés toutes les heures
   - Consultez et modérez les articles dans l'admin

3. **Gestion des utilisateurs** :
   - Visualisez les utilisateurs et leurs préférences
   - Consultez les logs d'emails envoyés

## Tâches automatiques

Les tâches Celery suivantes s'exécutent automatiquement :

- **Récupération d'articles** : Toutes les heures
- **Envoi des digests quotidiens** : Tous les jours à 8h00
- **Envoi des digests hebdomadaires** : Lundi à 8h00
- **Envoi des digests bi-hebdomadaires** : Lundi et jeudi à 8h00
- **Envoi des digests tri-hebdomadaires** : Lundi, mercredi et vendredi à 8h00

## Structure du projet

```
News-Paper/
├── backend/                # Backend Django
│   ├── config/            # Configuration du projet
│   ├── users/             # App de gestion des utilisateurs
│   ├── articles/          # App de gestion des articles
│   ├── subscriptions/     # App de gestion des abonnements
│   ├── manage.py
│   └── requirements.txt
├── frontend/              # Frontend React
│   ├── src/
│   │   ├── components/   # Composants UI (shadcn/ui)
│   │   ├── contexts/     # Contextes React (Auth)
│   │   ├── lib/          # Utilitaires
│   │   ├── pages/        # Pages de l'application
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── docker-compose.yml     # Configuration Docker Compose
└── README.md
```

## API Endpoints

### Authentification
- `POST /api/users/register/` - Inscription
- `POST /api/users/login/` - Connexion (retourne JWT tokens)
- `POST /api/users/token/refresh/` - Rafraîchir le token

### Utilisateur
- `GET /api/users/profile/` - Profil utilisateur
- `PATCH /api/users/profile/` - Mettre à jour le profil
- `POST /api/users/change-password/` - Changer le mot de passe

### Centres d'intérêt
- `GET /api/users/interests/` - Liste des centres d'intérêt
- `GET /api/users/my-interests/` - Centres d'intérêt de l'utilisateur
- `POST /api/users/my-interests/add/` - Ajouter un centre d'intérêt
- `DELETE /api/users/my-interests/{id}/` - Retirer un centre d'intérêt

### Articles
- `GET /api/articles/` - Liste des articles (filtrés par intérêts)
- `GET /api/articles/{id}/` - Détails d'un article
- `GET /api/articles/saved/` - Articles sauvegardés
- `GET /api/articles/liked/` - Articles aimés
- `POST /api/articles/{id}/save/` - Sauvegarder un article
- `POST /api/articles/{id}/unsave/` - Retirer des favoris
- `POST /api/articles/{id}/like/` - Aimer un article
- `POST /api/articles/{id}/unlike/` - Retirer le like

### Abonnements
- `GET /api/subscriptions/` - Préférences d'abonnement
- `PATCH /api/subscriptions/` - Mettre à jour les préférences
- `POST /api/subscriptions/unsubscribe/` - Se désabonner
- `POST /api/subscriptions/resubscribe/` - Se réabonner
- `GET /api/subscriptions/logs/` - Logs d'emails

## Développement

### Backend

Pour exécuter les tests :
```bash
cd backend
python manage.py test
```

### Frontend

Pour builder l'application :
```bash
cd frontend
npm run build
```

Pour prévisualiser le build :
```bash
npm run preview
```

## Production

### Checklist avant le déploiement

1. Changez `SECRET_KEY` dans les variables d'environnement
2. Définissez `DEBUG=False`
3. Configurez `ALLOWED_HOSTS` avec votre domaine
4. Utilisez PostgreSQL au lieu de SQLite
5. Configurez un vrai serveur SMTP pour les emails
6. Utilisez HTTPS
7. Configurez les fichiers statiques avec un CDN ou serveur de fichiers
8. Mettez en place des sauvegardes régulières de la base de données

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

## Licence

MIT License

## Support

Pour toute question ou problème, veuillez ouvrir une issue sur GitHub.

---

Développé avec ❤️ par l'équipe News Paper