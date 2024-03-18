from pgvector.psycopg import register_vector
import psycopg
from sentence_transformers import SentenceTransformer


# DEFINE THE DATABASE CREDENTIALS
user = 'testuser'
password = 'testpwd'
host = 'localhost'
port = 5432
database = 'vectordb'

db_url = f"postgresql://{user}:{password}@{host}:{port}/{database}"


conn = psycopg.connect(conninfo=db_url)

conn.execute('CREATE EXTENSION IF NOT EXISTS vector')
register_vector(conn)

conn.execute('DROP TABLE IF EXISTS documents_test')
conn.execute('CREATE TABLE documents_test (id bigserial PRIMARY KEY, content text, embedding vector(384))')

input = [
    'The dog is barking',
    'The cat is purring',
    'The bear is growling'
]

model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(input, show_progress_bar=True)



for content, embedding in zip(input, embeddings):
    conn.execute('INSERT INTO documents_test (content, embedding) VALUES (%s, %s)', (content, embedding))

conn.commit()

document_id = 1
neighbors = conn.execute('SELECT content FROM documents_test WHERE id != %(id)s ORDER BY embedding <=> (SELECT embedding FROM documents_test WHERE id = %(id)s) LIMIT 5', {'id': document_id}).fetchall()
for neighbor in neighbors:
    print(neighbor[0])

conn.close()