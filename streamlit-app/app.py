# Python In-built packages
import time 

# External packages
import streamlit as st
import pandas as pd
import psycopg
from pgvector.psycopg import register_vector
from sentence_transformers import SentenceTransformer

# Identifiants de connection à la BDD PostgreSQL + pgvector
import os
from dotenv import load_dotenv
load_dotenv() 
# user = os.environ['DB_USER']
# password = os.environ['DB_PWD']
# host = os.environ['DB_HOST']
# port = os.environ['DB_PORT']
# database = os.environ['DB_NAME']

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
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Test DB Connection ---
def test_connection():
    with psycopg.connect(conninfo=db_url) as conn:
        res = conn.execute("""SELECT * FROM version();""").fetchall()
        psql_ver = res[0][0]
        return psql_ver
    
st.success(f"**Connecté à la base de données** : {test_connection()}")


# Modèle Sentence Transformer pour l'encodage de la requète de recherche
# Modèle pré-entraîné d'encodage de textes en français
model_name = "dangvantuan/sentence-camembert-base" # vector size = 768

@st.cache_resource(show_spinner=False)  # 👈 Add the caching decorator
def load_model(model_name):
    return SentenceTransformer(model_name)
model = load_model(model_name)

# Retourner les résultats dans une DataFrame
@st.cache_data(show_spinner=False)  # 👈 Add the caching decorator
def query_to_dataframe(query, column_names, top_k=10):

    # Connect to an existing database
    with psycopg.connect(conninfo=db_url) as conn:

        register_vector(conn)

        query_embedding = model.encode(query)

        res = conn.execute(f"""
            SELECT
                1 - (embedding <=> %s) AS cosine_similarity,
                id,    
                question,
                reponse
            FROM piaf ORDER BY cosine_similarity DESC LIMIT {top_k};
        """, (query_embedding, )).fetchall()

        res_df = pd.DataFrame(res, columns=column_names)
        
        return res_df

st.title('🔎 Recherche sémantique')

"""
Recherche sémantique dans une base de donnée PostgreSQL avec l'extension [pgvector](https://github.com/pgvector/pgvector).

- Jeu de données : [Piaf v1.2](https://www.data.gouv.fr/en/datasets/piaf-le-dataset-francophone-de-questions-reponses/)
- Modèle : [Sentence Transformers](https://www.sbert.net/index.html) [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
"""
with st.form(key="search-form"):
    query = st.text_input('Recherche', placeholder="Entrez votre recherche ici")
    submit = st.form_submit_button('Rechercher')

if submit : 
    with st.container():
        star_time = time.time()
        res_df = query_to_dataframe(query, ['cosine_similarity', 'id', 'question', 'reponse'])
        st.dataframe(res_df)
        end_time = time.time()
        st.write(f"Temps de la recherche : {round(end_time - star_time, 2)} secondes")