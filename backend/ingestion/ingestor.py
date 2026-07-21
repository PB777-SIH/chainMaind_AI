import io
import json
import os
import sys
import zipfile

# 📍 Tell Python to look one directory up (in backend/) for database.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import database  # 👈 The red line will disappear!
import pandas as pd
import processor
import requests


def get_latest_gkg_url():
  """Finds the URL for the most recent 15-minute GKG file from GDELT."""
  master_list_url = "http://data.gdeltproject.org/gdeltv2/lastupdate.txt"
  try:
    response = requests.get(master_list_url)
    # GDELT updates have 3 lines (export, mentions, gkg). We want gkg.
    lines = response.text.split("\n")
    gkg_line = [l for l in lines if "gkg.csv.zip" in l][0]
    return gkg_line.split(" ")[2]
  except Exception as e:
    print(f"❌ Error fetching GDELT master list: {e}")
    return None


def fetch_and_filter_gkg(url):
  """Downloads, unzips in-memory, and filters news for Semiconductor keywords."""
  print(f"📥 Fetching latest news from: {url}")
  response = requests.get(url)

  # Use zipfile to handle GDELT's .zip format in-memory
  with zipfile.ZipFile(io.BytesIO(response.content)) as z:
    csv_filename = z.namelist()[0]
    with z.open(csv_filename) as f:
      # GKG 2.0 uses TAB (\t) as a delimiter
      df = pd.read_csv(
          f, sep="\t", header=None, low_memory=False, encoding="utf-8"
      )

  # Keywords targeting Industrial Friction and key Semiconductor Entities
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

  # Column 7 = Themes, Column 3 = Organizations
  mask = df[7].str.contains("|".join(keywords), na=False, case=False) | df[
      3
  ].str.contains("|".join(keywords), na=False, case=False)

  filtered_df = df[mask]
  print(f"🎯 Filtered {len(filtered_df)} relevant industrial events.")
  return filtered_df


if __name__ == "__main__":
  # 1. Get the URL for the latest GDELT batch
  latest_url = get_latest_gkg_url()

  if latest_url:
    # 2. Download and Filter
    data = fetch_and_filter_gkg(latest_url)

    # 3. Analyze the first hit with AI (if data exists)
    if not data.empty:
      # Column 4 in GKG 2.0 is the DocumentIdentifier (The actual URL)
      sample_news_url = data.iloc[0][4]
      print(f"🧐 Analyzing top event: {sample_news_url}")

      # Call the AI logic in processor.py
      intelligence = processor.extract_risk_intelligence(sample_news_url)

      print("\n" + "=" * 30)
      print("🤖 AI RISK INTELLIGENCE")
      print("=" * 30)
      print(intelligence)
      print("=" * 30)

      # 4. Save to PostgreSQL Database
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
        except Exception as e:
          print(f"❌ Could not save to database: {e}")
    else:
      print("📭 No semiconductor-related news in this 15-minute window.")