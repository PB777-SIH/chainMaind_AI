import os
import requests
import json
from groq import Groq
from dotenv import load_dotenv
import database

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# --- OPTION 1: CLOUD AI (Groq) ---
def extract_risk_intelligence(news_text):
    """Sends raw news to Groq for structured Risk Intelligence."""
    system_prompt = """
        You are the Analyst Assistant inside ChainMind AI, an AI-driven semiconductor supply-chain risk platform.
        Respond with ONLY a JSON object in this exact shape:
        {
            "primary_entity": (string, the main company/entity discussed, e.g., "TSMC"),
            "impact_score": (float, 0.0 to 1.0, representing severity),
            "event_type": (string, e.g., "SUPPLY_CHAIN_BOTTLENECK", "EXPANSION"),
            "summary": (string, a concise 1-sentence summary of the news)
        }
    """
    try:
        completion = groq_client.chat.completions.create(
            model="openai/gpt-oss-20b",  # Universally accessible model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Analyze this: {news_text}"}
            ],
            response_format={"type": "json_object"}
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"❌ Groq Error in News Extraction: {e}")
        return None

# --- OPTION 2: LOCAL AI (Ollama) ---
def extract_risk_local(news_text):
    """Uses local Llama 3.1 to analyze risk at $0 cost."""
    print("🏠 Using ollama for analysis...")
    url = "http://localhost:11434/api/generate"
    prompt = f"Analyze this news for semiconductor supply chain risk: {news_text}. Return ONLY a JSON object with impact_score, primary_entity, event_type, and summary."
    
    payload = {
        "model": "llama3.1",
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }
    try:
        response = requests.post(url, json=payload)
        return response.json()['response']
    except Exception as e:
        print(f"❌ Ollama Error: {e}")
        return None

# --- OPTION 3: CHAT RAG ---
def answer_analyst_question(question, context=None):
  """Open-ended Q&A for the Analyst Assistant chat using PostgreSQL RAG + Groq AI."""

  # 1. Retrieve knowledge base facts from Postgres
  db_records = database.query_knowledge_base(question)

  kb_context_str = ""
  if db_records:
    kb_context_str = "\n".join([
        f"- [{r['category']}] {r['entity_name']}: {r['details']}"
        for r in db_records
    ])
  else:
    kb_context_str = "No specific database matches found."

  # 2. Relaxed prompt allowing general domain knowledge
  system_prompt = """
    You are the Analyst Assistant inside ChainMind AI, an expert semiconductor supply-chain risk intelligence platform.

    - Ground your answer in the provided [DATABASE KNOWLEDGE BASE CONTEXT] or [FRONTEND DASHBOARD CONTEXT] whenever relevant.
    - For general industry queries (e.g., why TSMC/ASML are critical, manufacturing bottlenecks, or definitions), seamlessly supplement with your general domain knowledge.
    - Keep answers concise (2-4 sentences), factual, and directly related to supply chain risks.

    Respond with ONLY a JSON object in this exact shape:
    {
      "response": (string, 2-4 sentences, plain language, no markdown),
      "cited_sources": (array of short strings naming sources used, e.g. ["PostgreSQL Knowledge Base"] or ["General Knowledge"]),
      "current_node_context": (string: the single entity name, e.g. "TSMC", or null)
    }
    """

  user_prompt = f"""
    [DATABASE KNOWLEDGE BASE CONTEXT]
    {kb_context_str}

    [FRONTEND DASHBOARD CONTEXT]
    {json.dumps(context or {}, indent=2)}

    [USER QUESTION]
    {question}
    """

  try:
    completion = groq_client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
    )
    return json.loads(completion.choices[0].message.content)
  except Exception as e:
    print(f"❌ Groq Chat Error: {e}")
    return {
        "response": f"🚨 RAW ERROR DETECTED: {str(e)}",
        "cited_sources": [],
        "current_node_context": None,
    }