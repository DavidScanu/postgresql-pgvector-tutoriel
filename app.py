# Python In-built packages
import time 
# import os
# import uuid

# External packages
import streamlit as st
import pandas as pd
import psycopg
from sentence_transformers import SentenceTransformer

# Identifiants de connection à la BDD PostgreSQL + pgvector
user = 'testuser'
password = 'testpwd'
host = 'localhost'
port = 5432
database = 'vectordb'
db_url = f"postgresql://{user}:{password}@{host}:{port}/{database}"

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Recherche sémantique",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modèle Sentence Transformer pour l'encodage de la requète de recherche
model_name = 'all-MiniLM-L6-v2' # Vector size = 384

# A propos du caching
# https://docs.streamlit.io/library/advanced-features/caching

@st.cache_resource(show_spinner=False)  # 👈 Add the caching decorator
def load_model(model_name):
    return SentenceTransformer(model_name, device='cuda')
model = load_model(model_name)

# Retourner les résultats dans une DataFrame
@st.cache_data(show_spinner=False)  # 👈 Add the caching decorator
def query_to_dataframe(query, column_names):

    # Connect to an existing database
    with psycopg.connect(conninfo=db_url) as conn:
        # Open a cursor to perform database operations
        with conn.cursor() as cur:
            embeddings_query = model.encode(query).tolist()
            # Execute a command: this creates a new table
            res = cur.execute("""
                SELECT
                    1 - (embedding <=> %s) AS cosine_similarity,
                    id,    
                    question,
                    reponse
                FROM piaf ORDER BY cosine_similarity DESC LIMIT 10;
            """, (str(embeddings_query), )).fetchall()
    res_df = pd.DataFrame(res, columns=column_names)
    return res_df

st.title('🔎 Recherche sémantique')

"""
Recherche sémantique dans une base de donnée PostgreSQL avec l'extension [pgvector](https://github.com/pgvector/pgvector).

- Jeu de données : [Piaf v1.2](https://www.data.gouv.fr/en/datasets/piaf-le-dataset-francophone-de-questions-reponses/)
- Modèle : [Sentence Transformers](https://www.sbert.net/index.html) [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
"""

query = st.text_input('Recherche', placeholder="Entrez votre recherche ici")

if query : 
    star_time = time.time()
    res_df = query_to_dataframe(query, ['cosine_similarity', 'id', 'question', 'reponse'])
    st.dataframe(res_df)
    end_time = time.time()
    st.write(f"Temps de la recherche : {round(end_time - star_time, 2)} secondes")