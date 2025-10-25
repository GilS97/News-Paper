# Guide de démarrage rapide - News Paper

Ce guide vous permet de lancer l'application en quelques minutes.

## Lancement rapide avec Docker

1. **Démarrez l'application** :
```bash
docker-compose up --build
```

2. **Accédez à l'application** :
   - Frontend : http://localhost
   - Backend API : http://localhost:8000
   - Admin Django : http://localhost:8000/admin

3. **Créez un superutilisateur** (dans un nouveau terminal) :
```bash
docker-compose exec backend python manage.py createsuperuser
```

4. **Ajoutez des données de test** :
   - Connectez-vous à l'admin : http://localhost:8000/admin
   - Ajoutez des centres d'intérêt (Interests)
   - Ajoutez des sources d'articles (Sources)

### Exemples de sources RSS à ajouter

| Nom | URL | Type | Centres d'intérêt |
|-----|-----|------|-------------------|
| TechCrunch | https://techcrunch.com/feed/ | RSS | Technologie |
| Science Daily | https://www.sciencedaily.com/rss/all.xml | RSS | Science |
| Le Monde Tech | https://www.lemonde.fr/pixels/rss_full.xml | RSS | Technologie |
| ArXiv CS | http://export.arxiv.org/rss/cs | RSS | Science, Technologie |

### Exemples de centres d'intérêt

- Technologie
- Science
- Intelligence Artificielle
- Programmation
- Data Science
- Cybersécurité
- Cloud Computing
- DevOps

## Utilisation

1. **Créez un compte utilisateur** :
   - Allez sur http://localhost
   - Cliquez sur "S'inscrire"
   - Remplissez le formulaire

2. **Configurez vos préférences** :
   - Cliquez sur l'icône "Settings"
   - Sélectionnez vos centres d'intérêt
   - Configurez la fréquence des emails

3. **Explorez les articles** :
   - Les articles apparaîtront sur votre dashboard
   - Utilisez la barre de recherche pour filtrer
   - Sauvegardez vos articles préférés
   - Aimez les articles intéressants

## Lancer la récupération d'articles manuellement

Pour tester immédiatement sans attendre la tâche planifiée :

```bash
docker-compose exec backend python manage.py shell
```

Puis dans le shell Python :
```python
from articles.tasks import fetch_new_articles
fetch_new_articles()
```

## Dépannage

### Le frontend ne se charge pas
- Vérifiez que le port 80 n'est pas utilisé
- Consultez les logs : `docker-compose logs frontend`

### Le backend ne répond pas
- Vérifiez que le port 8000 n'est pas utilisé
- Consultez les logs : `docker-compose logs backend`

### Pas d'articles dans le feed
1. Vérifiez que vous avez ajouté des sources dans l'admin
2. Vérifiez que vous avez sélectionné des centres d'intérêt
3. Lancez manuellement la récupération d'articles (voir ci-dessus)

### Celery ne fonctionne pas
- Vérifiez que Redis est en cours d'exécution : `docker-compose logs redis`
- Vérifiez Celery worker : `docker-compose logs celery`
- Vérifiez Celery beat : `docker-compose logs celery-beat`

## Arrêter l'application

```bash
docker-compose down
```

Pour supprimer aussi les volumes (données) :
```bash
docker-compose down -v
```

## Lancement sans Docker (Développement)

### Backend

1. Créez un environnement virtuel :
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. Lancez les migrations :
```bash
python manage.py migrate
```

4. Créez un superutilisateur :
```bash
python manage.py createsuperuser
```

5. Lancez le serveur :
```bash
python manage.py runserver
```

6. Dans des terminaux séparés :
```bash
# Terminal 2: Redis
redis-server

# Terminal 3: Celery worker
celery -A config worker -l info

# Terminal 4: Celery beat
celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

### Frontend

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

## Prochaines étapes

- Consultez le README.md pour la documentation complète
- Explorez l'API : http://localhost:8000/api/
- Personnalisez les templates d'emails dans `backend/subscriptions/tasks.py`
- Ajoutez plus de sources d'articles

Bon développement ! 🚀
