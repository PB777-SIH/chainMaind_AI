from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.database import get_recent_alerts
from backend.fusion.fusion_engine import FusionEngine
from backend.economics.market_tracker import fetch_market_signals
from backend.graph.neo4j_setup import SemiconductorGraph
from backend.ingestion.processor import answer_analyst_question
from backend.simulation.optimizer import SupplyChainOptimizer
from backend.ingestion.ingestor import run_ingestion # Assuming this is the correct path


app = FastAPI(title="ChainMind AI API", version="1.0.0")

allowed_origins = os.getenv(
    "ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:5174"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

fusion_engine = None
graph_db = None

class ChatRequest(BaseModel):
    query: str
    context: Optional[Dict[str, Any]] = {}

class ScenarioRequest(BaseModel):
    disrupted_node: str
    disruption_type: str
    severity: float
    target_node: Optional[str] = "Apple"


@app.on_event("startup")
def startup_event():
    global fusion_engine, graph_db
    
    # 1. Initialize Databases First
    try:
        fusion_engine = FusionEngine()
        print("✅ FusionEngine and Neo4j driver initialized successfully.")
    except Exception as e:
        print(f"⚠️ Warning: FusionEngine connection failed: {e}")

    try:
        graph_db = SemiconductorGraph()
        print("✅ SemiconductorGraph initialized successfully.")
    except Exception as e:
        print(f"⚠️ Warning: SemiconductorGraph connection failed: {e}")
        
    # 2. Run News Ingestion 
    print("⚡ Running startup news ingestion...")
    try:
        run_ingestion()
        print("✅ Startup news ingestion complete.")
    except Exception as e:
        print(f"⚠️ Startup ingestion skipped/failed: {e}")


@app.on_event("shutdown")
def shutdown_event():
    if fusion_engine and hasattr(fusion_engine, "close"):
        fusion_engine.close()
    if graph_db and hasattr(graph_db, "close"):
        graph_db.close()


@app.get("/")
def health_check():
    return {"status": "online", "system": "ChainMind AI Core"}


@app.get("/api/fusion/risk")
def get_fused_risk(
    entity_id: str = "default",
    nlp_risk: float = 0.5,
    graph_impact: float = 0.5,
    econ_volatility: float = 0.5,
    satellite_signal: float = 0.5,
):
    if not fusion_engine:
        raise HTTPException(status_code=500, detail="FusionEngine not initialized")
    try:
        risk_score = fusion_engine.calculate_fused_risk(
            nlp_risk, graph_impact, econ_volatility, satellite_signal
        )
        return {
            "entity_id": entity_id,
            "risk_score": risk_score,
            "inputs": {"nlp": nlp_risk, "graph": graph_impact, "econ": econ_volatility, "satellite": satellite_signal},
            "status": "success",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/graph-risk")
def api_graph_risk(target_entity: str = "TSMC"):
    if not fusion_engine:
        raise HTTPException(status_code=500, detail="FusionEngine not initialized")
    try:
        return fusion_engine.run_pipeline(target_entity=target_entity)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/entities")
def api_entities():
    if not graph_db:
        raise HTTPException(status_code=500, detail="Graph not initialized")
    try:
        return graph_db.get_all_entities()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/materials")
def api_materials():
    try:
        return fetch_market_signals()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/alerts")
def api_alerts(limit: int = 20):
    try:
        return get_recent_alerts(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/scenario")
def api_scenario(req: ScenarioRequest):
    optimizer = SupplyChainOptimizer()
    try:
        return optimizer.run_what_if_scenario(req.disrupted_node, req.target_node)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        optimizer.close()


@app.post("/api/chat")
def api_chat(req: ChatRequest):
    try:
        return answer_analyst_question(req.query, context=req.context)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))