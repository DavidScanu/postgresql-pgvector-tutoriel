# Créer une base de données vectorielle avec PostgreSLQ et pgvector (Docker)

Démonstration d'implémentation d'une **recherche vectorielle** avec PostgreSQL, l'extension `pgvector` et Python. 

## Etapes

1. Créer la BDD PostgreSQL + pgvector dans un conteneur Docker
2. Se connecter avec psql (pour vérification)
3. Importer les données (textes)
4. Créer les vecteurs avec Sentence Transformers
5. Créer une table 'quora' dans la BDD
6. Sauvegarder les données et les vecteurs dans la BDD
7. Utiliser la recherche vectorielle 

## Utilisation

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

Le notebook se connecte à la base de donnée locale et effectue des requète SQL avec `psycopg`.

## Todo 
 
- Faire marcher Sentence Transformers en local
- Changer de jeu de données (100 000 lignes en français)
- Ajouter un indexing (hsnwlib ou IVFFlat)
- Filtering

## Ressources 

- https://access.crunchydata.com/documentation/pgvector/0.5.1/
- https://github.com/pgvector/pgvector
- https://www.enterprisedb.com/blog/what-is-pgvector
- https://medium.com/@johannes.ocean/setting-up-a-postgres-database-with-the-pgvector-extension-10ab7ff212cc
- https://devcenter.heroku.com/articles/pgvector-heroku-postgres#negative-inner-product
- https://blog.heroku.com/pgvector-for-similarity-search-on-heroku-postgres