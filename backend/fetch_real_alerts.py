import os
import json
import urllib.parse
import feedparser
from groq import Groq
from database import get_db_connection

# Initialize Groq client using GROQ_API_KEY from environment
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

TARGET_KEYWORDS = ["TSMC", "ASML", "Samsung Foundry", "Intel Foundry", "semiconductor shortage"]

def classify_headline_with_groq(headline: str) -> dict:
    """Uses Groq LLM to extract risk parameters from a headline."""
    prompt = f"""
    Analyze this semiconductor news headline:
    "{headline}"

    Return JSON strictly matching this structure:
    {{
        "primary_entity": "TSMC or ASML or Samsung Foundry or Intel Foundry or Hsinchu Science Park or Global",
        "risk_score": 0.75,
        "event_type": "GEOPOLITICAL_RISK or ENVIRONMENTAL_RISK or SUPPLY_CHAIN_BOTTLENECK or UTILITY_DISRUPTION"
    }}
    """
    try:
        response = groq_client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"⚠️ Groq classification warning for '{headline[:30]}...': {e}")
        return {
            "primary_entity": "Global",
            "risk_score": 0.50,
            "event_type": "SUPPLY_CHAIN_BOTTLENECK"
        }

def fetch_and_save_real_news():
    conn = get_db_connection()
    cur = conn.cursor()

    # Clear old alerts so the feed stays fresh
    cur.execute("DELETE FROM alerts;")

    total_inserted = 0

    for keyword in TARGET_KEYWORDS:
        encoded_query = urllib.parse.quote(f'"{keyword}" supply chain OR risk OR delay')
        rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
        
        feed = feedparser.parse(rss_url)

        for entry in feed.entries[:2]:
            headline = entry.title
            link = entry.link

            # 1. Classify with Groq LLM
            classification = classify_headline_with_groq(headline)

            # 2. Extract values
            entity = classification.get("primary_entity", keyword)
            risk_score = float(classification.get("risk_score", 0.50))
            event_type = classification.get("event_type", "SUPPLY_CHAIN_BOTTLENECK")

            # 3. Save to PostgreSQL using correct column name 'entity'
            cur.execute("""
                INSERT INTO alerts (entity, risk_score, event_type, summary, url)
                VALUES (%s, %s, %s, %s, %s)
            """, (entity, risk_score, event_type, headline, link))
            
            total_inserted += 1
            print(f"✅ Classified & Added: [{entity}] {headline[:60]}...")

    conn.commit()
    cur.close()
    conn.close()
    print(f"\n🎉 Success! Inserted {total_inserted} real, LLM-classified news alerts into PostgreSQL.")

if __name__ == "__main__":
    fetch_and_save_real_news()