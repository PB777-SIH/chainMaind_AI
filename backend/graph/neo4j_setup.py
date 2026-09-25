from neo4j import GraphDatabase
import os
import time
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")


class SemiconductorGraph:
    def __init__(self):
        self.uri = "bolt://127.0.0.1:7687"
        self.user = "neo4j"
        self.password = os.getenv("NEO4J_PASSWORD", "expert_password")
        self.driver = None

        retries = 12
        while retries > 0:
            try:
                candidate = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
                candidate.verify_connectivity()
                self.driver = candidate  # only keep it once it's actually proven to work
                break
            except Exception:
                print(f"⏳ Neo4j is still booting up (Java engine loading)... waiting 5 seconds. ({retries} attempts left)")
                retries -= 1
                time.sleep(5)

        if not self.driver:
            print("❌ Failed to connect. Please check Docker Desktop to ensure chainmind_neo4j is running.")





    

    def close(self):
        if self.driver:
            self.driver.close()

    def build_digital_twin(self):
        """Creates the initial Nodes and Edges for the Supply Chain."""
        if not self.driver:
            return

        print("🕸️ Mapping the Semiconductor Supply Chain in Neo4j...")

        # cypher_query = """
        #     CREATE (asml:EquipmentMaker {name: 'ASML', country: 'Netherlands', lat: 51.42, lng: 5.40, risk_score: 0.22})
        #     CREATE (tsmc:Foundry {name: 'TSMC', country: 'Taiwan', lat: 24.77, lng: 120.97, risk_score: 0.81})
        #     CREATE (nvidia:DesignHouse {name: 'NVIDIA', country: 'USA', lat: 37.37, lng: -121.96, risk_score: 0.42})
        #     CREATE (apple:DesignHouse {name: 'Apple', country: 'USA', lat: 37.33, lng: -122.01, risk_score: 0.38})
        #     CREATE (hsinchu:Region {name: 'Hsinchu Science Park', country: 'Taiwan', lat: 24.79, lng: 120.99, risk_score: 0.74})
        #     CREATE (port_kaohsiung:Port {name: 'Port of Kaohsiung', country: 'Taiwan', lat: 22.62, lng: 120.30, risk_score: 0.69})

        #     CREATE (asml)-[:SUPPLIES_TO]->(tsmc)
        #     CREATE (asml)-[:DEPENDS_ON_EQUIPMENT]->(tsmc)
        #     CREATE (tsmc)-[:SUPPLIES_TO]->(nvidia)
        #     CREATE (tsmc)-[:SUPPLIES_TO]->(apple)
        #     CREATE (tsmc)-[:LOCATED_IN]->(hsinchu)
        #     CREATE (tsmc)-[:LOCATED_IN]->(port_kaohsiung)
        # """
        # cypher_query = """
        #     MERGE (asml:EquipmentMaker {name: 'ASML'}) SET asml.country='Netherlands', asml.lat=51.42, asml.lng=5.40, asml.risk_score=0.22
        #     MERGE (tsmc:Foundry {name: 'TSMC'}) SET tsmc.country='Taiwan', tsmc.lat=24.77, tsmc.lng=120.97, tsmc.risk_score=0.81
        #     MERGE (nvidia:DesignHouse {name: 'NVIDIA'}) SET nvidia.country='USA', nvidia.lat=37.37, nvidia.lng=-121.96, nvidia.risk_score=0.42
        #     MERGE (apple:DesignHouse {name: 'Apple'}) SET apple.country='USA', apple.lat=37.33, apple.lng=-122.01, apple.risk_score=0.38
        #     MERGE (hsinchu:Region {name: 'Hsinchu Science Park'}) SET hsinchu.country='Taiwan', hsinchu.lat=24.79, hsinchu.lng=120.99, hsinchu.risk_score=0.74
        #     MERGE (port_kaohsiung:Port {name: 'Port of Kaohsiung'}) SET port_kaohsiung.country='Taiwan', port_kaohsiung.lat=22.62, port_kaohsiung.lng=120.30, port_kaohsiung.risk_score=0.69

        #     MERGE (asml)-[:SUPPLIES_TO]->(tsmc)
        #     MERGE (asml)-[:DEPENDS_ON_EQUIPMENT]->(tsmc)
        #     MERGE (tsmc)-[:SUPPLIES_TO]->(nvidia)
        #     MERGE (tsmc)-[:SUPPLIES_TO]->(apple)
        #     MERGE (tsmc)-[:LOCATED_IN]->(hsinchu)
        #     MERGE (tsmc)-[:LOCATED_IN]->(port_kaohsiung)
        #"""

        cypher_query = """
    MERGE (asml:EquipmentMaker {name: 'ASML'}) SET asml.country='Netherlands', asml.lat=51.42, asml.lng=5.40, asml.risk_score=0.22
    MERGE (tsmc:Foundry {name: 'TSMC'}) SET tsmc.country='Taiwan', tsmc.lat=24.77, tsmc.lng=120.97, tsmc.risk_score=0.81
    MERGE (nvidia:DesignHouse {name: 'NVIDIA'}) SET nvidia.country='USA', nvidia.lat=37.37, nvidia.lng=-121.96, nvidia.risk_score=0.42
    MERGE (apple:DesignHouse {name: 'Apple'}) SET apple.country='USA', apple.lat=37.33, apple.lng=-122.01, apple.risk_score=0.38
    MERGE (samsung:Foundry {name: 'Samsung Foundry'}) SET samsung.country='South Korea', samsung.lat=37.00, samsung.lng=127.03, samsung.risk_score=0.58
    MERGE (intel:Foundry {name: 'Intel Foundry'}) SET intel.country='USA', intel.lat=45.52, intel.lng=-122.67, intel.risk_score=0.35
    MERGE (hsinchu:Region {name: 'Hsinchu Science Park'}) SET hsinchu.country='Taiwan', hsinchu.lat=24.79, hsinchu.lng=120.99, hsinchu.risk_score=0.74
    MERGE (port_kaohsiung:Port {name: 'Port of Kaohsiung'}) SET port_kaohsiung.country='Taiwan', port_kaohsiung.lat=22.62, port_kaohsiung.lng=120.30, port_kaohsiung.risk_score=0.69

    MERGE (asml)-[:SUPPLIES_TO]->(tsmc)
    MERGE (asml)-[:DEPENDS_ON_EQUIPMENT]->(tsmc)
    MERGE (tsmc)-[:SUPPLIES_TO]->(nvidia)
    MERGE (tsmc)-[:SUPPLIES_TO]->(apple)
    MERGE (tsmc)-[:LOCATED_IN]->(hsinchu)
    MERGE (tsmc)-[:LOCATED_IN]->(port_kaohsiung)
    """

        with self.driver.session() as session:
            session.run(cypher_query)
            print("✅ Digital Twin initialized successfully!")

    def get_all_entities(self):
        """Returns every graph node shaped for the frontend globe:
        {id, name, type, lat, lng, risk_score, status, country}"""
        if not self.driver:
            return []

        query = """
            MATCH (n)
            WHERE n.lat IS NOT NULL AND n.lng IS NOT NULL
            RETURN n.name AS name, labels(n)[0] AS type,
                   n.lat AS lat, n.lng AS lng,
                   n.risk_score AS risk_score, n.country AS country
        """
        with self.driver.session() as session:
            results = session.run(query)
            entities = []
            for row in results:
                risk = row["risk_score"] if row["risk_score"] is not None else 0.1
                status = "critical" if risk >= 0.65 else "warn" if risk >= 0.4 else "ok"
                entities.append({
                    "id": row["name"].lower().replace(" ", "-"),
                    "name": row["name"],
                    "type": row["type"],
                    "lat": row["lat"],
                    "lng": row["lng"],
                    "risk_score": risk,
                    "status": status,
                    "country": row["country"],
                })
            return entities


if __name__ == "__main__":
    db = SemiconductorGraph()
    try:
        db.build_digital_twin()
    finally:
        db.close()