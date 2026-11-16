from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.app.api.interview_data import INTERVIEW_QUESTIONS

router = APIRouter(prefix="/interview", tags=["Interview Lab"])

class VerifyAnswerRequest(BaseModel):
    question_id: str
    selected_option_index: int

@router.get("/questions")
def get_questions(category: Optional[str] = None, difficulty: Optional[str] = None):
    results = []
    for q in INTERVIEW_QUESTIONS:
        if category and q["category"].lower() != category.lower():
            continue
        if difficulty and q["difficulty"].lower() != difficulty.lower():
            continue
        # Strip correct answer from listing for clean client-side testing
        safe_q = dict(q)
        # We don't expose correct_option_index in client listing to prevent cheating
        safe_q.pop("correct_option_index", None)
        safe_q.pop("explanation", None)
        safe_q.pop("why_incorrect", None)
        safe_q.pop("follow_up_answer", None)
        results.append(safe_q)
    return results

@router.get("/categories")
def get_interview_categories():
    categories = sorted(list(set(q["category"] for q in INTERVIEW_QUESTIONS)))
    return categories

@router.post("/verify")
def verify_answer(req: VerifyAnswerRequest):
    for q in INTERVIEW_QUESTIONS:
        if q["id"] == req.question_id:
            is_correct = (req.selected_option_index == q["correct_option_index"])
            return {
                "question_id": req.question_id,
                "is_correct": is_correct,
                "selected_option_index": req.selected_option_index,
                "correct_option_index": q["correct_option_index"],
                "explanation": q["explanation"],
                "why_incorrect": q["why_incorrect"],
                "follow_up": q.get("follow_up"),
                "follow_up_answer": q.get("follow_up_answer"),
                "related_concept": q.get("related_concept"),
                "scenario_link": q.get("scenario_link")
            }
    raise HTTPException(status_code=404, detail="Question not found")

