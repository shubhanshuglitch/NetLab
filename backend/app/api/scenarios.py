from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException
from backend.app.scenarios.scenario_definitions import get_default_scenarios

router = APIRouter(prefix="/scenarios", tags=["Scenarios"])

@router.get("")
def list_scenarios(category: Optional[str] = None):
    scenarios = get_default_scenarios()
    res = []
    for s in scenarios:
        if category and s["category"].lower() != category.lower():
            continue
        res.append({
            "id": s["id"],
            "category": s["category"],
            "title": s["title"],
            "difficulty": s["difficulty"],
            "summary": s["summary"],
            "core_concept": s["core_concept"],
            "key_question": s["key_question"],
            "node_count": len(s["topology"].devices),
            "link_count": len(s["topology"].links)
        })
    return res

@router.get("/{scenario_id}")
def get_scenario(scenario_id: str):
    scenarios = get_default_scenarios()
    for s in scenarios:
        if s["id"] == scenario_id:
            return s
    raise HTTPException(status_code=404, detail="Scenario not found")
