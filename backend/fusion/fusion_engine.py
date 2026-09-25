import os
import sys
from dotenv import load_dotenv
from neo4j import GraphDatabase

# 📍 Ensure Python can import from backend root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import database
from economics.market_tracker import get_economic_risk_score
from geospatial.satellite_sensor import get_satellite_risk_score

load_dotenv()


class FusionEngine:

  def __init__(self):
    self.uri = "bolt://127.0.0.1:7687"
    self.user = "neo4j"
    self.password = os.getenv("NEO4J_PASSWORD", "expert_password")
    self.driver = GraphDatabase.driver(
        self.uri, auth=(self.user, self.password)
    )

  def close(self):
    self.driver.close()

  def calculate_fused_risk(
      self, nlp_risk, graph_impact, econ_volatility, satellite_signal
  ):
    """Fuses 4 distinct modalities into a single metric using the Phase 5 weighting formula."""
    total_risk = (
        (0.4 * nlp_risk)
        + (0.3 * graph_impact)
        + (0.2 * econ_volatility)
        + (0.1 * satellite_signal)
    )
    return round(total_risk, 4)

  def propagate_risk_in_graph(self, origin_entity, origin_risk):
    """Expert Move: Propagates risk downstream through Neo4j graph edges (-[:SUPPLIES_TO]->)."""
    query = """
            MATCH p = (origin {name: $entity})-[:SUPPLIES_TO*1..2]->(downstream)
            RETURN downstream.name AS downstream_entity, 
                   labels(downstream)[0] AS entity_type,
                   length(p) AS hops
            """
    attenuation_factor = (
        0.80  # Risk diminishes slightly with each supply chain hop
    )

    with self.driver.session() as session:
      results = session.run(query, entity=origin_entity)
      propagated_events = []
      for row in results:
        hops = row["hops"]
        downstream_name = row["downstream_entity"]

        # Calculate attenuated downstream risk
        impacted_risk = round(origin_risk * (attenuation_factor**hops), 4)
        propagated_events.append({
            "entity": downstream_name,
            "type": row["entity_type"],
            "inherited_risk": impacted_risk,
            "hops_from_source": hops,
        })
      return propagated_events

  def run_pipeline(
      self,
      target_entity="TSMC",
      sample_nlp_score=0.85,
      sample_centrality_score=0.60,
  ):
    print(f"🧬 EXECUTING MULTI-MODAL FUSION ENGINE FOR: [{target_entity}]")
    print("=" * 65)

    # 1. Collect Live Signals from Phase 3 & Phase 4
    econ_score = get_economic_risk_score()
    sat_score = get_satellite_risk_score(
        location_name=f"{target_entity} Facility"
    )

    print(f"📡 Sensor Modality Inputs:")
    print(f"   ├─ Phase 1 (NLP Risk):        {sample_nlp_score:.2f}")
    print(f"   ├─ Phase 2 (Graph Impact):    {sample_centrality_score:.2f}")
    print(f"   ├─ Phase 3 (Econ Volatility): {econ_score:.2f}")
    print(f"   └─ Phase 4 (Satellite Signal):{sat_score:.2f}")

    # 2. Compute Fused Total Risk
    fused_risk = self.calculate_fused_risk(
        sample_nlp_score, sample_centrality_score, econ_score, sat_score
    )
    print("-" * 65)
    print(f"🔥 TOTAL FUSED RISK SCORE: {fused_risk:.4f} / 1.0000")
    print("=" * 65)

    # 3. Trigger Downstream Risk Propagation if Threshold Exceeded (> 0.40)
    # if fused_risk >= 0.40:
    #   print(
    #       f"⚠️ HIGH RISK THRESHOLD EXCEEDED! Propagating graph risk from"
    #       f" [{target_entity}]..."
    #   )
    #   downstream_impacts = self.propagate_risk_in_graph(
    #       target_entity, fused_risk
    #   )

    #   if downstream_impacts:
    #     print("\n🌊 DOWNSTREAM RISK PROPAGATION FLOW:")
    #     for impact in downstream_impacts:
    #       print(
    #           f"   🌊 [Hop {impact['hops_from_source']}] {impact['entity']}"
    #           f" ({impact['type']}) ---> Propagated Risk:"
    #           f" {impact['inherited_risk']:.4f}"
    #       )
    #   else:
    #     print("   ℹ️ No downstream supply-chain connections found in graph.")
    # else:
    #   print("✅ Risk within safe operational thresholds. No propagation.")

    # fusion_engine.py — inside run_pipeline(), replace the final block with:
    result = {
        "total_fused_risk": fused_risk,
        "weights": {"nlp": 0.4, "graph": 0.3, "econ": 0.2, "satellite": 0.1},
        "propagated_impacts": [],
    }

    if fused_risk >= 0.40:
      print(f"⚠️ HIGH RISK THRESHOLD EXCEEDED! Propagating graph risk from [{target_entity}]...")
      downstream_impacts = self.propagate_risk_in_graph(target_entity, fused_risk)
      result["propagated_impacts"] = downstream_impacts

      if downstream_impacts:
        print("\n🌊 DOWNSTREAM RISK PROPAGATION FLOW:")

        for impact in downstream_impacts:
          print(f"   🌊 [Hop {impact['hops_from_source']}] {impact['entity']} ({impact['type']}) ---> Propagated Risk: {impact['inherited_risk']:.4f}")

      else:
        print("   ℹ️ No downstream supply-chain connections found in graph.")

    else:
      print("✅ Risk within safe operational thresholds. No propagation.")

    return result
  
if __name__ == "__main__":
  engine = FusionEngine()
  try:
    # Run simulation assuming high NLP alert on TSMC
    engine.run_pipeline(
        target_entity="TSMC",
        sample_nlp_score=0.85,
        sample_centrality_score=0.60,
    )
  finally:
    engine.close()