from typing import List, Dict, Any
from fastapi import APIRouter
from backend.app.api.concepts import CONCEPTS_CATALOG
from backend.app.scenarios.scenario_definitions import get_default_scenarios
from backend.app.api.interview_data import INTERVIEW_QUESTIONS

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("")
def search_all(q: str):
    q_lower = q.lower().strip()
    if not q_lower:
        return {"concepts": [], "scenarios": [], "interview_questions": []}

    matched_concepts = []
    for c in CONCEPTS_CATALOG:
        text = f"{c['name']} {c['layer']} {c['summary']} {c['simple_explanation']} {c['real_world_application']}".lower()
        if q_lower in text:
            matched_concepts.append(c)

    matched_scenarios = []
    for s in get_default_scenarios():
        text = f"{s['title']} {s['category']} {s['summary']} {s['core_concept']} {s['key_question']} {s['explanation']}".lower()
        if q_lower in text:
            matched_scenarios.append({
                "id": s["id"],
                "category": s["category"],
                "title": s["title"],
                "difficulty": s["difficulty"],
                "summary": s["summary"],
                "core_concept": s["core_concept"],
                "key_question": s["key_question"]
            })

    matched_questions = []
    for q_item in INTERVIEW_QUESTIONS:
        text = f"{q_item['question']} {q_item['category']} {q_item.get('related_concept', '')}".lower()
        if q_lower in text:
            matched_questions.append({
                "id": q_item["id"],
                "category": q_item["category"],
                "difficulty": q_item["difficulty"],
                "question": q_item["question"],
                "related_concept": q_item.get("related_concept")
            })

    return {
        "query": q,
        "concepts": matched_concepts[:5],
        "scenarios": matched_scenarios[:5],
        "interview_questions": matched_questions[:8]
    }

