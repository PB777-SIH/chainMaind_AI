import os
import requests
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# --- OPTION 1: CLOUD AI (Groq) ---
def extract_risk_intelligence(news_text):
    """Sends raw news to Groq for ultra-fast structured Risk Intelligence."""
    system_prompt = """
    You are a Senior Supply Chain Risk Analyst. 
    Analyze the news and return ONLY a JSON object:
    {
      "impact_score": (float 0-1),
      "primary_entity": (string),
      "event_type": (string),
      "summary": (string)
    }
    """
    try:
        completion = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Analyze this: {news_text}"}
            ],
            response_format={"type": "json_object"}
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"❌ Groq Error: {e}")
        return None

# --- OPTION 2: LOCAL AI (Ollama) ---
def extract_risk_local(news_text):
    """Uses local Llama 3.1 to analyze risk at $0 cost."""
    print("🏠 Using local Ollama for analysis...")
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