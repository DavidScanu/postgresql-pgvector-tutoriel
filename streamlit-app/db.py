import os
import time

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import psycopg
from pgvector.psycopg import register_vector
import torch 


# -- Importer le jeu de données (textes) --

# question-reponse-sans-texte.csv
dataset_url = "https://www.data.gouv.fr/fr/datasets/r/14159082-d1be-417e-a67c-c3c494c7a4ad"
dataset_df = pd.read_csv(dataset_url)
corpus_questions = dataset_df.loc[:, 'question'].tolist()
corpus_reponses = dataset_df.loc[:, 'reponse'].tolist()

# Afficher les 10 premières paires de question-réponse.
for question, reponse in zip(corpus_questions[:10], corpus_reponses[:10]):
    print(f"{question} => {reponse}")


# -- Encoder les questions avec Sentence Transformers --

# Modèle Sentence Transformer pour l'encodage du jeu de données ou de la requète de recherche sémantique
# Modèle pré-entraîné d'encodage de textes en français
model_name = "dangvantuan/sentence-camembert-base" # vector size = 768

# Utilisation du GPU si disponible
if torch.cuda.is_available():
    model = SentenceTransformer(model_name, device='cuda')
else:
    model = SentenceTransformer(model_name)

# Encodage vectoriel des questions avec Sentence Transformer
questions_embeddings = model.encode(corpus_questions, show_progress_bar=True)


## -- Sauvegarder les données et les vecteurs dans la BDD --

# Identifiants de connexion à la base de données
user = 'testuser'
password = 'testpwd'
host = 'localhost'
port = 5432
database = 'vectordb'
db_url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
print("PostgreSQL DB URI :", db_url)

# Vérification de la connexion à la base de données
with psycopg.connect(conninfo=db_url) as conn:
    res = conn.execute("""
    SELECT * FROM version();
    """).fetchall()
    for row in res :
        print("Connecté à la base de données :", row[0])
        
# Sauvegarde des questions/reponses et des vecteurs des questions
with psycopg.connect(conninfo=db_url) as conn:
    # Activation de l'extension pgvector (si elle n'existe pas déjà)
    conn.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    # Enregistrez le type 'vecteur' avec votre connexion
    register_vector(conn)
    # Effacement de la table (si elle n'existe pas déjà)
    conn.execute("""DROP TABLE IF EXISTS piaf CASCADE;""")
    # Création de la table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS piaf (
            id serial PRIMARY KEY,
            question text NOT NULL,
            reponse text NOT NULL,
            embedding vector(768) NOT NULL,
            created_at timestamptz DEFAULT now()
            );
        """)
    # Sauvegarde des questions/reponses et des vecteurs des questions
    for question, reponse, embedding in zip(corpus_questions, corpus_reponses, questions_embeddings):
        conn.execute("""INSERT INTO piaf (question, reponse, embedding) VALUES (%s, %s, %s);""", (question, reponse, embedding))
    # Ajouter un index (recherche approximative)
    # conn.execute('CREATE INDEX IF NOT EXISTS idx_piaf_hnsw ON piaf USING hnsw (embedding vector_cosine_ops) WITH (m = 8, ef_construction = 24);')
    # Rendre les changements dans la base de données persistents
    conn.commit()


## -- Utiliser la recherche vectorielle -- 

query = "quelle est la date de la libération ?"
# Encoder la requète avec Sentence Transformers
embedding_query = model.encode(query)
# Recherche de questions similaires dans la base de données
with psycopg.connect(conninfo=db_url) as conn:
    # Enregistrez le type 'vecteur' avec votre connexion
    register_vector(conn)
    # Executer la commande
    res = conn.execute("""
        SELECT
            id,
            1 - (embedding <=> %s) AS cosine_similarity,
            question,
            reponse
        FROM piaf ORDER BY cosine_similarity DESC LIMIT 10;
    """, (embedding_query, )).fetchall()

    for row in res:
        print(f"id : {row[0]} | score : {round(row[1], 4)} | Question : {row[2]} | Réponse : {row[3]}")