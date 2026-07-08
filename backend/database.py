import psycopg2
import os
import json
from dotenv import load_dotenv

# Load the .env file so we don't hardcode passwords
load_dotenv()

def get_db_connection():
    """Connects to Postgres using variables from .env"""
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("POSTGRES_DB", "chainmind_db"),
        user=os.getenv("POSTGRES_USER", "poshika"),
        password=os.getenv("POSTGRES_PASSWORD", "expert_password")
    )

def create_tables():
    """Creates the 'alerts' table."""
    conn = get_db_connection()
    cur = conn.cursor()
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
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Database Table 'alerts' is ready!")

def insert_alert(entity, score, event, summary, url):
    """Saves a single AI finding into the database."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO alerts (entity, risk_score, event_type, summary, url)
        VALUES (%s, %s, %s, %s, %s)
    """, (entity, score, event, summary, url))
    conn.commit()
    cur.close()
    conn.close()
    print(f"💾 Saved alert for {entity} to Database!")

if __name__ == "__main__":
    create_tables()