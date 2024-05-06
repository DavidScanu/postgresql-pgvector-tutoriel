CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS piaf (
  id serial PRIMARY KEY,
  question text NOT NULL,
  reponse text NOT NULL,
  embedding vector(768) NOT NULL,
  created_at timestamptz DEFAULT now()
);