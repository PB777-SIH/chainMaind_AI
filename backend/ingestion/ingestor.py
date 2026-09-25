from datetime import datetime, timedelta, timezone
import io
import json
import os
import sys
import zipfile

# Tell Python to look one directory up (in backend/) for database.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import database
from ingestion import processor
import pandas as pd
import requests


def get_latest_gkg_url():
  """Fetches the latest GKG file from GDELT.

  If the newest file advertises a 404, automatically walks back 15-minute
  intervals to find the latest valid batch.
  """
  master_list_url = "http://data.gdeltproject.org/gdeltv2/lastupdate.txt"

  # 1. Try lastupdate.txt first
  try:
    response = requests.get(master_list_url, timeout=10)
    lines = response.text.split("\n")
    gkg_line = [l for l in lines if "gkg.csv.zip" in l][0]
    raw_url = gkg_line.split(" ")[2].strip().replace("http://", "https://")

    # Check if file actually exists on CDN
    check = requests.head(raw_url, timeout=5)
    if check.status_code == 200:
      return raw_url
    print(
        f"⚠️ GDELT advertised file returned {check.status_code}. Walking back to"
        " previous 15-min batch..."
    )
  except Exception as e:
    print(
        f"⚠️ Could not read lastupdate.txt: {e}. Switching to time fallback..."
    )

  # 2. Fallback: Walk backward in 15-minute chunks to find the newest working batch
  now = datetime.now(timezone.utc)
  minute = (now.minute // 15) * 15
  base_time = now.replace(minute=minute, second=0, microsecond=0)

  for i in range(1, 8):  # Check up to 2 hours back
    fallback_time = base_time - timedelta(minutes=15 * i)
    timestamp = fallback_time.strftime("%Y%m%d%H%M00")
    fallback_url = (
        f"https://data.gdeltproject.org/gdeltv2/{timestamp}.gkg.csv.zip"
    )

    try:
      res = requests.head(fallback_url, timeout=5)
      if res.status_code == 200:
        print(f"✅ Found active GDELT batch: {fallback_url}")
        return fallback_url
    except Exception:
      continue

  return None


def fetch_and_filter_gkg(url):
  """Downloads, unzips in-memory, and filters news for Semiconductor keywords."""
  if not url:
    print("❌ No valid GDELT batch URL available.")
    return pd.DataFrame()

  print(f"📥 Fetching news from: {url}")

  try:
    response = requests.get(url, timeout=20)
    response.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
      csv_filename = z.namelist()[0]
      with z.open(csv_filename) as f:
        df = pd.read_csv(
            f, sep="\t", header=None, low_memory=False, encoding="utf-8"
        )

  except Exception as e:
    print(f"❌ Failed to process GDELT file: {e}")
    return pd.DataFrame()

  keywords = [
      "SEMICONDUCTOR",
      "LITHOGRAPHY",
      "TSMC",
      "ASML",
      "CHIP_SHORTAGE",
      "NVIDIA",
      "INTEL",
      "FABRICATION",
  ]

  mask = df[7].str.contains("|".join(keywords), na=False, case=False) | df[
      3
  ].str.contains("|".join(keywords), na=False, case=False)

  filtered_df = df[mask]
  print(f"🎯 Filtered {len(filtered_df)} relevant industrial events.")
  return filtered_df


def run_ingestion():
  """Main entry point to fetch news, run AI risk extraction, and save to PostgreSQL."""
  latest_url = get_latest_gkg_url()

  if latest_url:
    data = fetch_and_filter_gkg(latest_url)

    if not data.empty:
      sample_news_url = data.iloc[0][4]
      print(f"🧐 Analyzing top event: {sample_news_url}")

      intelligence = processor.extract_risk_intelligence(sample_news_url)

      print("\n" + "=" * 30)
      print("🤖 AI RISK INTELLIGENCE")
      print("=" * 30)
      print(intelligence)
      print("=" * 30)

      if intelligence:
        try:
          intel_dict = json.loads(intelligence)
          database.insert_alert(
              entity=intel_dict.get("primary_entity", "Unknown"),
              score=float(intel_dict.get("impact_score", 0.0)),
              event=intel_dict.get("event_type", "Unknown"),
              summary=intel_dict.get("summary", "No summary"),
              url=sample_news_url,
          )
          return intel_dict
        except Exception as e:
          print(f"❌ Could not save to database: {e}")
    else:
      print("📭 No semiconductor-related news found in this batch.")
  else:
    print("❌ Could not retrieve GDELT batch.")
  return None


if __name__ == "__main__":
  run_ingestion()