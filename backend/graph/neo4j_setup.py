from neo4j import GraphDatabase
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path="../.env")


class SemiconductorGraph:
    def __init__(self):
        # 💡 FIX 1: Use 127.0.0.1 instead of localhost
        self.uri = "bolt://127.0.0.1:7687"
        self.user = "neo4j"
        self.password = "expert_password"
        self.driver = None

        # 💡 FIX 2: The Patience Loop (Neo4j takes ~45 seconds to boot)
        retries = 12
        while retries > 0:
            try:
                self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
                self.driver.verify_connectivity()  # Test the connection
                break
            except Exception as e:
                print(
                    f"⏳ Neo4j is still booting up (Java engine loading)... waiting 5 seconds. ({retries} attempts left)")
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

        cypher_query =  """
            // Create Nodes
           CREATE (asml:EquipmentMaker {name: 'ASML', region: 'Netherlands'})
           CREATE (tsmc:Foundry {name: 'TSMC', region: 'Taiwan'})
           CREATE (nvidia:DesignHouse {name: 'NVIDIA', region: 'USA'})
           CREATE (apple:DesignHouse {name: 'Apple', region: 'USA'})
           CREATE (hsinchu:Region {name: 'Hsinchu Science Park'})
           CREATE (port_kaohsiung:Port {name: 'Port of Kaohsiung'})

            // Create Explicit Typed Relationships (The Nervous System)
            CREATE (asml)-[:SUPPLIES_TO]->(tsmc)
            CREATE (asml)-[:DEPENDS_ON_EQUIPMENT]->(tsmc)
            CREATE (tsmc)-[:SUPPLIES_TO]->(nvidia)
            CREATE (tsmc)-[:SUPPLIES_TO]->(apple)
            CREATE (tsmc)-[:LOCATED_IN]->(hsinchu)
            CREATE (tsmc)-[:LOCATED_IN]->(port_kaohsiung)
            """

        with self.driver.session() as session:
            session.run(cypher_query)
            print("✅ Digital Twin initialized successfully!")


if __name__ == "__main__":
    db = SemiconductorGraph()
    try:
        db.build_digital_twin()
    finally:
        db.close()