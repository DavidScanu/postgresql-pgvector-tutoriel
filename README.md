# 🔎 Créer une base de données vectorielle avec PostgreSLQ et pgvector (Docker)

Démonstration d'implémentation d'une **recherche vectorielle** avec PostgreSQL, l'extension `pgvector` et Python. 

## ⚡Features

- Configuration `docker-compose.yaml` pour **PostgreSQL avec l'extension pgvector**
- Code Python pour générer des representations vectorielles avec `Sentence Transformers`
- Code Python pour insérer des données dans la base de données
- Code Python pour créer une recherche vectorielle à l'aide de **pgvector**
- Application **Streamlit** de démonstration

## 🗨️ Utilisation

1. Cloner ce dépôt
2. Se placer dans le dossier
```
cd postgresql-pgvector-tutoriel/
```
3. Installer les dépendances 
```
pip install -r requirements.txt
```
4. Lancer le conteneur Docker avec
```
docker compose up -d
```
5. Se connecter à la base de donnée avec `psql` (pour vérifications)
    -  Aller dans le conteneur : `docker exec -it <container id> bash`
    - Se connecter à la BDD : `psql -h localhost -U postgres -d vectordb`
6. Exectuer le notebook de ce dépôt
7. Lancer l'application **Streamlit**

Le notebook se connecte à la base de donnée locale et effectue des requète SQL avec `psycopg`.

## 💻 Application Streamlit

Après avoir executé le notebook, la commande suivante lance une application Streamlit avec laquelle vous pouvez effectuer une recherche sémantique dans la base de donnée.

```
streamlit run app.py
```

## 📑 Todo 
 
- Ajouter un indexing (hsnwlib ou IVFFlat)
- Filtering

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

### Psycopg 3

- [Psycopg 3 – PostgreSQL database adapter for Python](https://www.psycopg.org/psycopg3/docs/basic/usage.html)