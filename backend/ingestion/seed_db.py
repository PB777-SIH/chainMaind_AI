import json
import os
import sys

import pandas as pd

# Connect to database.py in backend/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import database


def seed_database():
  current_dir = os.path.dirname(os.path.abspath(__file__))
  json_path = os.path.join(current_dir, "seed_materials_routes.json")
  csv_path = os.path.abspath(os.path.join(current_dir, "..", "metadata.csv"))

  # Ensure DB tables exist
  database.create_tables()

  seeded_count = 0

  # 1. Seed metadata.csv (Company Profiles)
  if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    for _, row in df.iterrows():
      content = (
          f"Company: {row['long_name']} ({row['ticker']})\n"
          f"Industry: {row['industry']} | Sector: {row['sector']}\n"
          f"Headquarters: {row['hq_city']}, {row['hq_country']}\n"
          f"Overview: {row['name']} operates in {row['industry']} based out of"
          f" {row['hq_country']}. Market Cap: ${row['market_cap_current']:,.0f}"
          f" USD."
      )
      metadata = {
          "ticker": str(row["ticker"]),
          "country": str(row["hq_country"]),
          "industry": str(row["industry"]),
      }
      database.insert_knowledge(
          entity=str(row["name"]),
          category="Company Metadata",
          content=content,
          metadata=metadata,
      )
      seeded_count += 1
    print(f"✅ Seeded {len(df)} companies from metadata.csv into PostgreSQL.")
  else:
    print(f"⚠️ Warning: metadata.csv not found at {csv_path}")

  # 2. Seed seed_materials_routes.json (Raw Materials & Critical Supply Routes)
  if os.path.exists(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
      materials_data = json.load(f)

    for item in materials_data:
      content = (
          f"Entity: {item['entity']} ({item['category']})\n"
          f"Impact & Details: {item['description']}\n"
          f"Key Nodes/Suppliers:"
          f" {', '.join(item.get('key_suppliers', item.get('key_nodes', [])))}"
      )
      metadata = {
          "criticality": item.get("criticality", 1.0),
          "key_suppliers": item.get("key_suppliers", []),
      }
      database.insert_knowledge(
          entity=item["entity"],
          category=item["category"],
          content=content,
          metadata=metadata,
      )
      seeded_count += 1
    print(
        f"✅ Seeded {len(materials_data)} material routes from JSON into"
        " PostgreSQL."
    )

  print(f"\n🎉 Total seeded entries in PostgreSQL: {seeded_count}")


if __name__ == "__main__":
  seed_database()