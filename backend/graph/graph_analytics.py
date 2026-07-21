import os
import time
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()


class GraphAnalytics:
    def __init__(self):
        self.uri = "bolt://127.0.0.1:7687"
        self.user = "neo4j"
        self.password = "expert_password"
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))

    def close(self):
        self.driver.close()

    def run_betweenness_centrality(self):
        """Projects the supply chain graph into GDS memory and calculates choke points."""
        print("📊 Projecting Digital Twin into GDS Memory...")

        # Cypher queries
        drop_existing_projection = "CALL gds.graph.drop('supplyChainGraph', false) YIELD graphName;"

        project_graph = """
                CALL gds.graph.project(
                    'supplyChainGraph',
                    '*',
                    '*'
                )
                YIELD graphName, nodeCount, relationshipCount;
                """

        calculate_centrality = """
        CALL gds.betweenness.stream('supplyChainGraph')
        YIELD nodeId, score
        RETURN gds.util.asNode(nodeId).name AS entity_name, 
               labels(gds.util.asNode(nodeId))[0] AS entity_type, 
               score
        ORDER BY score DESC
        LIMIT 10;
        """

        with self.driver.session() as session:
            # 1. Clean up old projections if present
            try:
                session.run(drop_existing_projection)
            except Exception:
                pass

            # 2. Project graph into memory
            res = session.run(project_graph).single()
            print(f"✅ In-Memory Projection Ready ({res['nodeCount']} nodes, {res['relationshipCount']} relationships)")

            # 3. Calculate Betweenness Centrality
            print("\n🔥 TOP GLOBAL SUPPLY CHAIN CHOKE POINTS (Betweenness Centrality):")
            print("=" * 60)
            results = session.run(calculate_centrality)
            for row in results:
                print(f"🎯 [{row['entity_type']}] {row['entity_name']} ---> Centrality Score: {row['score']:.4f}")
            print("=" * 60)

            # 4. Cleanup projection
            session.run(drop_existing_projection)


if __name__ == "__main__":
    analytics = GraphAnalytics()
    try:
        analytics.run_betweenness_centrality()
    finally:
        analytics.close()