import os
import sys
from neo4j import GraphDatabase


class SupplyChainOptimizer:
    def __init__(self):
        self.uri = "bolt://127.0.0.1:7687"
        self.user = "neo4j"
        self.password = "expert_password"
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))

    def close(self):
        self.driver.close()

    def seed_alternatives(self):
        """Adds competitor foundries to the graph for the optimizer to choose from."""
        query = """
        // Create alternative suppliers with specific cost and risk metrics
        MERGE (samsung:Foundry {name: 'Samsung Foundry', region: 'South Korea', cost_multiplier: 1.15, geo_risk: 0.20})
        MERGE (intel:Foundry {name: 'Intel Foundry', region: 'USA', cost_multiplier: 1.40, geo_risk: 0.05})

        // Ensure Apple exists and wire them up as alternative paths
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

        if not alternatives:
            print(f"❌ CRITICAL FAILURE: No alternative suppliers found for {target_node}. Supply chain broken.")
            return

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

        print("=" * 75)
        print(f"🏆 OPTIMAL REROUTE IDENTIFIED: Switching production to {best_option['name']} ({best_option['region']}).")
        print(f"   Reasoning: Achieves the lowest combined cost/risk penalty ({best_optimization_score:.3f}).")
        print("=" * 75)


if __name__ == "__main__":
    optimizer = SupplyChainOptimizer()
    try:
        # Step 1: Make sure the graph has alternative paths
        optimizer.seed_alternatives()

        # Step 2: Run the scenario
        optimizer.run_what_if_scenario(disrupted_node="TSMC", target_node="Apple")
    finally:
        optimizer.close()