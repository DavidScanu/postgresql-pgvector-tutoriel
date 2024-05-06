# 🔎 Créer une base de données vectorielle avec PostgreSLQ et pgvector

Démonstration d'implémentation d'une **recherche vectorielle** avec PostgreSQL et l'extension `pgvector`. 

## ⚡Features

- Configuration `docker-compose.yaml` pour **PostgreSQL avec l'extension pgvector**.
- Code Python pour générer des representations vectorielles avec `Sentence Transformers`.
- Code Python pour insérer des données dans la base de données.
- Code Python pour créer une recherche vectorielle à l'aide de **pgvector**.
- Application **Streamlit** de démonstration.

## 🗨️ Utilisation

1. Clonez ce dépôt
```
git clone <url>
```
2. Placez-vous dans le dossier
```
cd postgresql-pgvector-tutoriel/
```
3. Lancez le conteneur 🐳 Docker avec
```
docker compose up -d
```
4. Déplacez-vous dans le dossier `streamlit-app` et installez les dépendances.

```bash
cd ./notebooks
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

5. Exécutez le fichier python `db.py` pour remplir la base de données.

```
python3 db.py
```


## 💻 Application Streamlit

Pour lancer l'application Streamlit, placez-vous dans le dossier `streamlit-app` et lancez la commande suivante :

```
streamlit run app.py
```

## Administrer la base de données

Deux méthodes pour contrôler la base de données PostgreSQL : [psql](https://docs.postgresql.fr/12/app-psql.html) ou [pgAdmin](https://www.pgadmin.org/).

## psql

Pour se connecter à la base de donnée avec `psql` (pour vérifications):
- Aller dans le conteneur : `docker exec -it <container id> bash`
- Se connecter à la BDD : `psql -h localhost -U  testuser -d vectordb`

## pgAdmin

Pour se connecter à la base de données avec `pgAdmin` : 

- Aller à l'adresse : `http://localhost:5050`
- Renseigner le nom et mot de passe pgAdmin déclarés dans le `docker-compose.yaml`
- Ajouter un nouveau serveur 
- Remplir les informations de connection : 
  - **Host name/address** : `db` (comme le nom du service dans le `docker-compose.yaml`)
  - **Port** : `5432`
  - **Username** : `testuser`
  - **Password** : `testpwd`

## 📑 Todo 
 
- App Streamlit dans un container
- Changer de dataset
- Ecrire un article de blog
- Ajouter un indexing (hsnwlib ou IVFFlat)
- Ajouter options de recherche (Filtering)

## 📺 Ressources 

### pgvector

- [pgvector GitHub](https://github.com/pgvector/pgvector)
- [pgvector crunchy data](https://access.crunchydata.com/documentation/pgvector/0.5.1/)
- [What is pgvector and How Can It Help You?](https://www.enterprisedb.com/blog/what-is-pgvector)
- [Implementing the pgvector extension for a PostgreSQL database](https://medium.com/@johannes.ocean/setting-up-a-postgres-database-with-the-pgvector-extension-10ab7ff212cc)
- [pgvector on Heroku Postgres](https://devcenter.heroku.com/articles/pgvector-heroku-postgres#negative-inner-product)
- [How to Use pgvector for Similarity Search on Heroku Postgres](https://blog.heroku.com/pgvector-for-similarity-search-on-heroku-postgres)
- [HNSW Indexes with Postgres and pgvector](https://www.crunchydata.com/blog/hnsw-indexes-with-postgres-and-pgvector)
- [Scaling Vector Data with Postgres](https://www.crunchydata.com/blog/scaling-vector-data-with-postgres)
- https://www.crunchydata.com/blog/topic/ai

### Psycopg 3

- [Psycopg 3 – PostgreSQL database adapter for Python](https://www.psycopg.org/psycopg3/docs/basic/usage.html)

### pgAdmin

- https://www.pgadmin.org/docs/pgadmin4/latest/container_deployment.html
