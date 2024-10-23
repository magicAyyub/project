# Backend FastAPI avec PostgreSQL et pgAdmin

## Description

Ce projet est un backend construit avec [FastAPI](https://fastapi.tiangolo.com/), utilisant [PostgreSQL](https://www.postgresql.org/) comme base de données et [pgAdmin](https://www.pgadmin.org/) pour gérer la base de données. Le tout est orchestré avec Docker pour faciliter le déploiement et l'exécution en local.

## Prérequis

Assurez-vous d'avoir les logiciels suivants installés :

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Configuration du projet

### 1. Clonez le repository

```bash
git clone https://github.com/magicAyyub/islah.git
cd islah/backend
```

### 2. Modifier le fichier `.env`

À la racine du répertoire `backend`, un fichier `.env` stock les variables d'environnement nécessaires pour PostgreSQL :

```env
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=mydatabase
```

Modifiez les valeurs de ces variables selon vos besoins. Ces valeurs seront utilisées pour initialiser la base de données PostgreSQL.

### 3. Construisez et démarrez les services (Uniquement pour la première fois ou après modification du Dockerfile)

Pour lancer l'application et les autres services (PostgreSQL et pgAdmin), exécutez :

```bash
sudo docker-compose up -d --build 
```

Cela démarrera les services définis dans `docker-compose.yml` :
- FastAPI : accessible via `http://localhost:8000`
- pgAdmin : accessible via `http://localhost:5050`

### 4. Accédez à l'application

- **FastAPI** : Rendez-vous à l'adresse `http://localhost:8000`.
- **Documentation Swagger UI** : Accessible à `http://localhost:8000/docs`.


### 5. Arrêter les services

Lorsque vous avez terminé, vous pouvez arrêter les services Docker avec :

```bash
sudo docker-compose down
```

Cela arrêtera les conteneurs tout en conservant les données (grâce aux volumes).

### 6. Reprendre le développement après redémarrage

Lorsque vous redémarrez votre machine ou après avoir arrêté les services, relancez simplement les conteneurs avec :

```bash
sudo docker-compose up -d
```

Cela démarre les services sans les reconstruire, ce qui est plus rapide.

### 7. Après un changement du schéma de la base de données

Faire une migration de la base de données

```bash
alembic revision --autogenerate -m "message de migration"
alembic upgrade head
```

### 8. Voir les logs

```bash
sudo docker-compose logs web 
```
# 9. Réinitialiser la base de données

```bash
sudo docker-compose down
sudo docker volume rm islah_backend_postgres-data
sudo docker-compose up -d
``` 


## Contributions

Les contributions sont les bienvenues ! N'hésitez pas à créer des issues ou à soumettre des pull requests pour améliorer ce projet.

## License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
