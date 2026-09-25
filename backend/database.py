import json
import os

from dotenv import load_dotenv
import psycopg2

load_dotenv()


def get_db_connection():
  """Connects to Postgres using variables from .env"""
  return psycopg2.connect(
      host=os.getenv("DB_HOST", "localhost"),
      database=os.getenv("POSTGRES_DB", "chainmind_db"),
      user=os.getenv("POSTGRES_USER", "poshika"),
      password=os.getenv("POSTGRES_PASSWORD", "expert_password"),
  )


def create_tables():
  """Creates 'alerts' and 'knowledge_base' tables if they don't exist."""
  conn = get_db_connection()
  cur = conn.cursor()

  # 1. Alerts Table
  cur.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id SERIAL PRIMARY KEY,
            entity VARCHAR(100),
            risk_score FLOAT,
            event_type VARCHAR(100),
            summary TEXT,
            url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

  # 2. Knowledge Base Table (Companies + Materials + Routes)
  cur.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_base (
            id SERIAL PRIMARY KEY,
            entity VARCHAR(150),
            category VARCHAR(100),
            content TEXT,
            metadata_json JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

  conn.commit()
  cur.close()
  conn.close()
  print("✅ Database tables ('alerts' & 'knowledge_base') are ready!")


def insert_alert(entity, score, event, summary, url):
  """Saves a single AI finding into the alerts table."""
  conn = get_db_connection()
  cur = conn.cursor()
  cur.execute(
      """
        INSERT INTO alerts (entity, risk_score, event_type, summary, url)
        VALUES (%s, %s, %s, %s, %s)
    """,
      (entity, score, event, summary, url),
  )
  conn.commit()
  cur.close()
  conn.close()


def insert_knowledge(entity, category, content, metadata=None):
  """Saves a knowledge chunk (company metadata, material route, etc.) into the database."""
  conn = get_db_connection()
  cur = conn.cursor()
  cur.execute(
      """
        INSERT INTO knowledge_base (entity, category, content, metadata_json)
        VALUES (%s, %s, %s, %s)
    """,
      (
          entity,
          category,
          content,
          json.dumps(metadata) if metadata else json.dumps({}),
      ),
  )
  conn.commit()
  cur.close()
  conn.close()


def search_knowledge(query_entity, limit=5):
  """Queries the knowledge base for matching entity details."""
  conn = get_db_connection()
  cur = conn.cursor()
  cur.execute(
      """
        SELECT entity, category, content, metadata_json 
        FROM knowledge_base 
        WHERE LOWER(entity) LIKE LOWER(%s) OR LOWER(content) LIKE LOWER(%s)
        LIMIT %s
    """,
      (f"%{query_entity}%", f"%{query_entity}%", limit),
  )
  rows = cur.fetchall()
  cur.close()
  conn.close()
  return [
      {"entity": r[0], "category": r[1], "content": r[2], "metadata": r[3]}
      for r in rows
  ]


def get_recent_alerts(limit=20):
  conn = get_db_connection()
  cur = conn.cursor()
  cur.execute(
      """
        SELECT id, entity, risk_score, event_type, summary, url, created_at
        FROM alerts ORDER BY created_at DESC LIMIT %s
    """,
      (limit,),
  )
  rows = cur.fetchall()
  cur.close()
  conn.close()
  return [
      {
          "id": r[0],
          "primary_entity": r[1],
          "impact_score": r[2],
          "event_type": r[3],
          "summary": r[4],
          "url": r[5],
          "timestamp": r[6].isoformat() if r[6] else None,
      }
      for r in rows
  ]


def query_knowledge_base(search_term: str):
  """Queries the knowledge_base table for relevant company or material route context."""
  import psycopg2
  from psycopg2.extras import RealDictCursor

  # Use your existing DB connection parameters/DATABASE_URL
  try:
    conn = get_db_connection()  # Uses your existing connection helper in database.py
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    query = """
            SELECT entity_name, category, details 
            FROM knowledge_base 
            WHERE entity_name ILIKE %s OR details ILIKE %s
            LIMIT 5;
        """
    pattern = f"%{search_term}%"
    cursor.execute(query, (pattern, pattern))
    results = cursor.fetchall()

    cursor.close()
    conn.close()
    return results
  except Exception as e:
    print(f"⚠️ Knowledge Base query error: {e}")
    return []

if __name__ == "__main__":
  create_tables()