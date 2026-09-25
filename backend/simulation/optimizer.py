import os
import sys
from neo4j import GraphDatabase


class SupplyChainOptimizer:
    def __init__(self):
        self.uri = "bolt://127.0.0.1:7687"
        self.user = "neo4j"
        self.password = os.getenv("NEO4J_PASSWORD", "expert_password")
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))

    def close(self):
        self.driver.close()

    def seed_alternatives(self):
        """Adds competitor foundries to the graph for the optimizer to choose from."""
        query = """
        MERGE (samsung:Foundry {name: 'Samsung Foundry'})
          SET samsung.region = 'South Korea', samsung.cost_multiplier = 1.15, samsung.geo_risk = 0.20
        MERGE (intel:Foundry {name: 'Intel Foundry'})
          SET intel.region = 'USA', intel.cost_multiplier = 1.40, intel.geo_risk = 0.05

        MERGE (apple:DesignHouse {name: 'Apple'})
        MERGE (samsung)-[:ALTERNATIVE_SUPPLIER]->(apple)
        MERGE (intel)-[:ALTERNATIVE_SUPPLIER]->(apple)
        """
        with self.driver.session() as session:
            session.run(query)
        print("✅ Added Intel (USA) and Samsung (South Korea) as alternative suppliers to Apple.")

    def run_what_if_scenario(self, disrupted_node, target_node):
        """Simulates a disruption and mathematically optimizes the best reroute."""
        print(f"\n🚨 SCENARIO INITIATED: What if [{disrupted_node}] is completely offline for 48 hours?")
        print("=" * 75)

        # Query Neo4j to find all alternative suppliers to the target node
        query = """
        MATCH (alt:Foundry)-[:ALTERNATIVE_SUPPLIER]->(target {name: $target_node})
        WHERE alt.name <> $disrupted_node
        RETURN alt.name AS name, alt.region AS region, 
               alt.cost_multiplier AS cost, alt.geo_risk AS risk
        """

        with self.driver.session() as session:
            results = session.run(query, target_node=target_node, disrupted_node=disrupted_node)
            alternatives = [record for record in results]

        # if not alternatives:
        #     print(f"❌ CRITICAL FAILURE: No alternative suppliers found for {target_node}. Supply chain broken.")
        #     return

        # optimizer.py — inside run_what_if_scenario(), replace the bare return
        if not alternatives:
            print(f"❌ CRITICAL FAILURE: No alternative suppliers found for {target_node}. Supply chain broken.")
            raise ValueError(f"No alternative suppliers found for {target_node}")

        print(f"🔍 Analyzing alternative routes for {target_node}...\n")

        best_option = None
        best_optimization_score = float('inf')  # We want the lowest score possible

        # Optimization Function (Minimizing Cost & Disruption Probability)
        for alt in alternatives:
            # Weighted formula: Heavily penalize high risk, while considering cost increases
            # Score = (Cost * 0.4) + (Risk * 0.6)
            optimization_score = (alt["cost"] * 0.4) + (alt["risk"] * 0.6)

            print(f"   🏭 Option: {alt['name']} ({alt['region']})")
            print(f"      ├─ Cost Multiplier: {alt['cost']}x")
            print(f"      ├─ Geo-Risk Factor: {alt['risk']}")
            print(f"      └─ 📊 Optimization Penalty Score: {optimization_score:.3f}")
            print("-" * 50)

            # If this is the lowest penalty score, it becomes the best option
            if optimization_score < best_optimization_score:
                best_optimization_score = optimization_score
                best_option = alt

        # optimizer.py — inside run_what_if_scenario(), after the for-loop, replace the final print block with:
        print("=" * 75)
        print(f"🏆 OPTIMAL REROUTE IDENTIFIED: Switching production to {best_option['name']} ({best_option['region']}).")
        print(f"   Reasoning: Achieves the lowest combined cost/risk penalty ({best_optimization_score:.3f}).")
        print("=" * 75)

        return {
            "target_entity": target_node,
            "disrupted_node": disrupted_node,
            "optimal_reroute": {
                "name": best_option["name"],
                "region": best_option["region"],
                "penalty_score": round(best_optimization_score, 3),
            },
            "alternatives": [
                {
                    "name": a["name"],
                    "cost_multiplier": a["cost"],
                    "geo_risk": a["risk"],
                    "penalty_score": round((a["cost"] * 0.4) + (a["risk"] * 0.6), 3),
                }
                for a in alternatives
            ],
        }


if __name__ == "__main__":
    optimizer = SupplyChainOptimizer()
    try:
        # Step 1: Make sure the graph has alternative paths
        optimizer.seed_alternatives()

        # Step 2: Run the scenario
        optimizer.run_what_if_scenario(disrupted_node="TSMC", target_node="Apple")
    finally:
        optimizer.close()