
# [Système de réservation de billets](https://www.ticket-booking.fxleclerc.com)

## Description

Ce projet est une application web de réservation de billets qui permet aux utilisateurs de consulter des événements, effectuer des réservations et gérer leur compte utilisateur.

**Important** :  
Ce projet a été réalisé dans un cadre scolaire.  
Il ne s’agit **pas d’un site web réel/fonctionnel**.
## Technologies

- **Backend** : Python, Flask
- **Base de données** : SQLite
- **ORM** : Flask-SQLAlchemy
- **Migrations** : Flask-Migrate (Alembic)
- **Authentification** : Flask sessions + bcrypt
- **Frontend** : HTML (Jinja2), CSS
- **Sécurité** : Flask-Talisman
- **Configuration** : python-dotenv (.env)
- **Serveur de production** : Gunicorn
- **Hébergement** : Render
## Fonctionnalités

### Routes
- **Authentification** : Signup, login, logout.
- **Événements** : Browsing, booking, paiement (simulé), cancellation.
- **Tableau utilisateur** : Résérvations avec date + statut, courriel, et changement de mot de passe.
- **Tableau administrateur** : Création, modification, suppression d'événements.

### Sécurité
- **Validation d'entrées utilisateur** : Formulaire de paiement, inscription, changement de mot de passe...
- **Protection CSRF** via tokens Flask-WTF.
- **Hashage** des mots de passe avec bcrypt.
- **Gestion des sessions** utilisateurs sécurisées.
- **Contrôle d’accès** basé sur les rôles.

### Backend
- **Structure en modules** (routes, modèles, utils).
- **Pattern factory** (create_app) pour initialisation de l’application.
- **ORM SQLAlchemy** pour gestion de la base de données.
- **Système de migration** de base de données (Flask-Migrate / Alembic).
- **Configuration centralisée** via classe Config et variables d’environnement.

### Base de données
- **Stockage** des utilisateurs, événements et réservations.
- **Relations** entre utilisateurs et réservations.
- **Gestion des statuts** de réservation (active, annulée).

### Frontend
- **Templates HTML** servis côté serveur (Jinja2).
- **Interface CSS** par section (événements, paiement, administration).
## Structure du projet

```text
.
│   .env                   # Variables d’environnement sensibles
│   .gitignore             # Fichiers ignorés par Git
│   LICENSE.txt              # License MIT
│   README.md              # Documentation
│   requirements.txt       # Dépendances Python
│   run.py                 # Point d’entrée pour lancer l’application
│
├───app                    # Dossier principal
│   │   config.py          # Configuration globale (clé secrète, DB, sécurité)
│   │   extensions.py      # Initialisation des extensions Flask (DB, Migrate)
│   │   __init__.py        # Création et configuration de l’app
│   │
│   ├───models             # Modèles de bases de données
│   │       __init__.py
│   │       booking.py     # Modèle de réservation
│   │       event.py       # Modèle d’événement
│   │       user.py        # Modèle utilisateur
│   │
│   ├───routes             # Définition des routes
│   │       __init__.py
│   │       admin_routes.py    # Routes admins (Tableau admin, création/modification d'événements...)
│   │       auth_routes.py     # Routes d’authentification (login/signup/logout)
│   │       booking_routes.py  # Routes liées aux réservations
│   │       event_routes.py    # Routes liées aux événements
│   │       user_routes.py     # Routes liées aux utilisateurs (Tableau utilisateur)
│   │
│   ├───static             # Fichiers statiques (CSS, images, etc.)
│   │   ├───css      # Styles CSS
│   │   │       style.css
│   │   │       events.css
│   │   │       modifier_event.css
│   │   │       simulation_paiement.css
│   │   │
│   │   └───img
│   │           favicon.ico    # Icône du site
│   │           favicon.png
│   │
│   ├───templates          # Templates HTML
│   │       base.html              # Template de base
│   │       index.html             # Page d’accueil
│   │       events.html            # Liste des événements
│   │       event.html             # Page d’événement spécifique
│   │       reservation.html       # Page de résérvation
│   │       simulation_paiement.html  # Page de paiement (simulé)
│   │       connexion.html         # Page de connexion
│   │       inscription.html       # Page d’inscription
│   │       tableau_admin.html     # Tableau de bord admin
│   │       tableau_utilisateur.html  # Tableau de bord utilisateur
│   │       modifier_event.html    # Page de modification d’événement
│   │
│   └───utils              # Fonctions utilitaires
│           __init__.py
│           auth.py        # Logique d’authentification (login, gestion de session)
│           security.py    # Fonctions de sécurité (validation, protection)
│
├───instance               # Données locales spécifiques à l’instance
│       site.db            # Base de données SQLite
└───migrations             # Gestion des migrations de base de données (Flask-Migrate/Alembic)
```
## Variables d'environnement

Pour ce projet, les variables suivantes doivent être ajoutées au fichier .env.

**Clés**

`SECRET_KEY`

`FLASK_ENV`

**Compte administrateur initial**

`ADMIN_EMAIL`

`ADMIN_PASSWORD`
## Auteurs

- [François-Xavier Leclerc](https://www.github.com/Jimpie1043)
- [Myriam Boulet](https://www.github.com/Mymytos)


## License

[MIT](https://choosealicense.com/licenses/mit/)