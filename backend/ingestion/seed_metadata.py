import os
import pandas as pd


def process_company_metadata(csv_path: str):
    """Parses metadata.csv into structured text documents for vector embeddings/RAG."""
    if not os.path.exists(csv_path):
        print(f"Error: Could not find '{csv_path}'")
        return []

    df = pd.read_csv(csv_path)
    documents = []

    for _, row in df.iterrows():
        content = (
            f"Company: {row['long_name']} ({row['ticker']})\n"
            f"Industry: {row['industry']} | Sector: {row['sector']}\n"
            f"Headquarters: {row['hq_city']}, {row['hq_country']}\n"
            f"Founded: {int(row['founded_year']) if pd.notna(row['founded_year']) else 'N/A'}\n"
            f"Overview: {row['name']} operates in {row['industry']} based out of {row['hq_country']}. "
            f"Market Cap: ${row['market_cap_current']:,.0f} USD. Website: {row['website']}"
        )

        metadata = {
            "entity": row["name"],
            "ticker": str(row["ticker"]),
            "country": str(row["hq_country"]),
            "industry": str(row["industry"]),
            "type": "company_metadata",
        }

        documents.append({"text": content, "metadata": metadata})

    return documents


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.abspath(os.path.join(current_dir, "..", "metadata.csv"))

    company_docs = process_company_metadata(csv_file)
    print(f"Loaded {len(company_docs)} company profiles for database seeding.")