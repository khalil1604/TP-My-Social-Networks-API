# My Social Networks API

API REST (type Facebook) réalisée dans le cadre du TP « My Social Networks API ».

**Stack :** FastAPI · Pydantic · SQLAlchemy · PostgreSQL

## Documentation de l'API (Swagger)

Une fois le serveur lancé : **http://127.0.0.1:8000/docs**

Swagger permet de voir tous les endpoints, leurs paramètres, les réponses possibles, et de les tester directement depuis le navigateur.

### Cloner et installer

```bash
git clone https://github.com/khalil1604/TP-My-Social-Networks-API
cd TP-My-Social-Networks-API
python -m venv venv ou uv init
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### Créer la base de données

Dans `psql` ou pgAdmin :

```sql
CREATE DATABASE tp_cours_api;
```

Configurer l'environnement

Copier  vers `.env`, puis renseigner son utilisateur et son mot de passe PostgreSQL :

```
DATABASE_URL=postgresql://UTILISATEUR:MOT_DE_PASSE@localhost:5432/social_api
```

### Lancer l'API

```bash
uvicorn app.main:app --reload
```

Les tables sont créées automatiquement au démarrage.

## Fonctionnalités réalisées

### Utilisateurs (CRUDS)

| Méthode | URL | Description |
|---|---|---|
| POST | `/users` | Créer un utilisateur (email unique) |
| GET | `/users` | Rechercher / lister (`q`, `skip`, `limit`) |
| GET | `/users/{id}` | Détail d'un utilisateur |
| PATCH | `/users/{id}` | Modifier un utilisateur |
| DELETE | `/users/{id}` | Supprimer un utilisateur |

### Événements (CRUDS)

| Méthode | URL | Description |
|---|---|---|
| POST | `/events` | Créer un événement (au moins 1 organisateur) |
| GET | `/events` | Rechercher / lister (`q`, `visibilite`, `skip`, `limit`) |
| GET | `/events/{id}` | Détail d'un événement et de ses membres |
| PATCH | `/events/{id}` | Modifier un événement |
| DELETE | `/events/{id}` | Supprimer un événement |
| POST | `/events/{id}/participants/{user_id}` | Ajouter un participant |
| DELETE | `/events/{id}/participants/{user_id}` | Retirer un participant |

### Règles 

- Deux utilisateurs ne peuvent pas avoir le même email (erreur `409`).
- Un événement a au moins un organisateur et un nombre quelconque de participants.
- Un utilisateur ne peut pas être ajouté deux fois au même événement (erreur `409`).
- La visibilité d'un événement est `public` ou `private`.

### Codes HTTP utilisés

`200` OK · `201` créé · `204` supprimé · `404` introuvable · `409` conflit · `422` données invalides

## Structure du projet

```
app/
├── main.py        # point d'entrée de l'API
├── config.py      # lecture du fichier .env
├── database.py    # connexion à PostgreSQL
├── models.py      # tables (SQLAlchemy)
├── schemas.py     # validation des données (Pydantic)
└── routers/
    ├── users.py   # routes des utilisateurs
    └── events.py  # routes des événements
```

## Reste à faire

Groupes · Fils de discussion · Albums photo · Sondages · Billetterie · Shopping list · Covoiturage (bonus) · Publication de la documentation Postman