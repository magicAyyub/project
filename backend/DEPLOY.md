# Étapes pour déployer FastAPI avec Docker sur un VPS Ubuntu

#### 1. **Configurer le VPS Ubuntu**

Commence par se connecter au  VPS Ubuntu en utilisant SSH. Les fournisseurs comme Hostinger, DigitalOcean ou AWS, donnent des instructions pour se connecter via SSH.

```bash
ssh username@ip_address_of_vps
```

#### 2. **Installer Docker et Docker Compose sur le VPS**

Si Docker et Docker Compose ne sont pas encore installés, installer en suivant ces étapes :

- **Installer Docker** :
  ```bash
  sudo apt update
  sudo apt install docker.io
  ```

- **Installer Docker Compose** :
  ```bash
  sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose
  ```

Vérifiez que Docker et Docker Compose sont correctement installés :

```bash
docker --version
docker-compose --version
```

#### 3. **Transférer le projet sur le VPS**

Utilisez soit `scp` ou Git pour transférer le projet sur le VPS.

- **Avec `scp` :**
  ```bash
  scp -r /chemin/local/vers/backend username@ip_address_of_vps:/chemin/destination
  ```

- **Avec Git :**
  ```bash
  git clone https://github.com/magicAyyub/islah.git
  cd islah/backend
  ```

#### 4. **Configurer le fichier `.env`**

Comme pour l'environnement local, à la racine du répertoire `backend`, un fichier `.env` stock les variables d'environnement nécessaires pour PostgreSQL :

```env
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=mydatabase
```
Modifiez les valeurs de ces variables selon vos besoins. Ces valeurs seront utilisées pour initialiser la base de données PostgreSQL.

#### 5. **Lancer Docker Compose sur le VPS**

Une fois que le projet est configuré sur le VPS, utilisez Docker Compose pour lancer les services comme fait localement :

```bash
sudo docker-compose up -d --build 
```

Cela lancera les conteneurs pour FastAPI, PostgreSQL et pgAdmin sur ton VPS.

#### 6. **Ouvrir les ports sur le VPS**

Assurez-vous que les ports nécessaires sont ouverts sur le VPS pour permettre l'accès à l'application depuis l'extérieur. Cela inclut généralement :

- **Port 8000** : Pour l'application FastAPI.
- **Port 5432** : Pour PostgreSQL (si nécessaire, `pas conseillé`).
- **Port 5050** : Pour pgAdmin (si vous voulez l'exposer à l'extérieur, `pas conseillé`).

Vous pouvez configurer le pare-feu sur Ubuntu avec `ufw` pour autoriser ces ports :

```bash
sudo ufw allow 8000
sudo ufw allow 5432
sudo ufw allow 5050
```

Ensuite, active le pare-feu si ce n'est pas déjà fait :

```bash
sudo ufw enable
```

#### 7. **Accéder à l'application depuis le navigateur**

Une fois les services lancés, vous devriez devrais pouvoir accéder à l'application FastAPI en utilisant l'IP du VPS dans le navigateur :

```
http://ip_address_of_vps:8000
```

également pgAdmin est accéder via :

```
http://ip_address_of_vps:5050
```

#### 8. **(Optionnel) Configurer un nom de domaine et SSL**

Pour rendre l'application accessible via un nom de domaine et sécuriser la connexion avec SSL, vous pouvez utiliser des services comme Nginx, Caddy ou Traefik. Ces services peuvent servir de proxy inverse pour rediriger le trafic HTTP/HTTPS vers l'application FastAPI.

#### 9. **Arrêter les services**

Lorsque vous avez terminé, vous pouvez arrêter les services Docker avec :

```bash
sudo docker-compose down
```

Cela arrêtera les conteneurs tout en conservant les données (grâce aux volumes).

#### 10. **Reprendre le développement après redémarrage**

Lorsque vous redémarrez votre machine ou après avoir arrêté les services, relancez simplement les conteneurs avec :

```bash
sudo docker-compose up -d
```


