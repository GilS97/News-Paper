# Guide de déploiement Docker - News Paper

## 🚀 Démarrage rapide

### Étape 1 : Nettoyer l'environnement (si nécessaire)

Si vous avez déjà lancé l'application auparavant :

```bash
# Arrêter tous les conteneurs
docker-compose down

# Supprimer les volumes (base de données, cache, etc.)
docker-compose down -v

# Nettoyer les images (optionnel)
docker system prune -a
```

### Étape 2 : Lancer l'application

```bash
# Construire et lancer tous les services
docker-compose up --build

# Ou en mode détaché (en arrière-plan)
docker-compose up --build -d
```

### Étape 3 : Vérifier que tout fonctionne

Attendez que tous les services soient démarrés. Vous devriez voir :

```
newspaper-redis          ... healthy
newspaper-backend        ... up
newspaper-celery-worker  ... up
newspaper-celery-beat    ... up
newspaper-frontend       ... up
```

Pour voir les logs en temps réel :
```bash
# Tous les services
docker-compose logs -f

# Un service spécifique
docker-compose logs -f backend
```

### Étape 4 : Créer le superutilisateur

```bash
docker-compose exec backend python manage.py createsuperuser
```

Suivez les instructions pour créer votre compte admin.

## 📋 Services disponibles

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost | Interface utilisateur React |
| Backend API | http://localhost:8000 | API Django REST |
| Admin Django | http://localhost:8000/admin | Interface d'administration |
| Redis | localhost:6379 | Cache et broker Celery |

## 🔧 Commandes utiles

### Gestion des conteneurs

```bash
# Voir l'état des conteneurs
docker-compose ps

# Arrêter les conteneurs
docker-compose stop

# Redémarrer les conteneurs
docker-compose restart

# Supprimer les conteneurs
docker-compose down
```

### Accéder au shell Django

```bash
docker-compose exec backend python manage.py shell
```

### Créer des migrations

```bash
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
```

### Collecter les fichiers statiques

```bash
docker-compose exec backend python manage.py collectstatic --noinput
```

### Tester Celery

```bash
# Vérifier les workers
docker-compose exec celery-worker celery -A config inspect active

# Vérifier les tâches planifiées
docker-compose exec celery-beat celery -A config inspect scheduled
```

## 🐛 Dépannage

### Le backend ne démarre pas

1. Vérifier les logs :
```bash
docker-compose logs backend
```

2. Vérifier que Redis est démarré :
```bash
docker-compose ps redis
```

3. Redémarrer le backend :
```bash
docker-compose restart backend
```

### Le frontend affiche une erreur 502

Cela signifie que nginx ne peut pas contacter le backend :

1. Vérifier que le backend est démarré :
```bash
docker-compose ps backend
```

2. Vérifier les logs du backend :
```bash
docker-compose logs backend
```

3. Redémarrer les services :
```bash
docker-compose restart backend frontend
```

### Celery ne traite pas les tâches

1. Vérifier les logs du worker :
```bash
docker-compose logs celery-worker
```

2. Vérifier que Redis est accessible :
```bash
docker-compose exec celery-worker redis-cli -h redis ping
```

3. Redémarrer Celery :
```bash
docker-compose restart celery-worker celery-beat
```

### Erreur "no such table"

Les migrations n'ont pas été exécutées :

```bash
docker-compose exec backend python manage.py migrate
```

### Réinitialiser complètement l'application

```bash
# Arrêter et supprimer tout
docker-compose down -v

# Supprimer les images
docker-compose down --rmi all

# Reconstruire et relancer
docker-compose up --build
```

## 📦 Structure des services

### Backend
- **Image** : Python 3.11-slim
- **Ports** : 8000
- **Volumes** :
  - Code source monté pour le développement
  - Fichiers statiques
  - Fichiers média
- **Healthcheck** : Attend que Redis soit prêt

### Celery Worker
- **Image** : Même que backend
- **Command** : `celery -A config worker`
- **Dépendances** : Redis, Backend

### Celery Beat
- **Image** : Même que backend
- **Command** : `celery -A config beat`
- **Dépendances** : Redis, Backend
- **Fonction** : Planification des tâches périodiques

### Frontend
- **Image** : Node 18 (build) + Nginx (production)
- **Ports** : 80
- **Build** : Multi-stage pour optimiser la taille

### Redis
- **Image** : Redis 7-alpine
- **Ports** : 6379
- **Healthcheck** : `redis-cli ping`

## 🔒 Production

Pour la production, modifiez les variables d'environnement :

1. Changez `SECRET_KEY` dans docker-compose.yml
2. Définissez `DEBUG=False`
3. Configurez `ALLOWED_HOSTS` avec votre domaine
4. Utilisez PostgreSQL au lieu de SQLite
5. Configurez un serveur SMTP réel pour les emails
6. Ajoutez HTTPS avec un reverse proxy (Caddy, Traefik)

## 📝 Variables d'environnement

Les variables importantes dans docker-compose.yml :

- `SECRET_KEY` : Clé secrète Django (CHANGEZ-LA EN PRODUCTION!)
- `DEBUG` : Mode debug (False en production)
- `ALLOWED_HOSTS` : Domaines autorisés
- `CELERY_BROKER_URL` : URL du broker Redis
- `CELERY_RESULT_BACKEND` : Backend pour les résultats Celery

## 🔄 Mise à jour de l'application

```bash
# Tirer les dernières modifications
git pull

# Reconstruire et redémarrer
docker-compose up --build -d

# Vérifier les logs
docker-compose logs -f
```

## 💾 Sauvegardes

### Sauvegarder la base de données

```bash
docker-compose exec backend python manage.py dumpdata > backup.json
```

### Restaurer la base de données

```bash
cat backup.json | docker-compose exec -T backend python manage.py loaddata --format=json -
```

---

Pour plus d'informations, consultez README.md
