from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from qna import answer_question
from explanation_module import explain_concept
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


# ============================================================
# Paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parent


# ============================================================
# FastAPI Application
# ============================================================

app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0",
)


# ============================================================
# Static Files and Templates
# ============================================================

app.mount(
    "/static",
    StaticFiles(
        directory=BASE_DIR / "static"
    ),
    name="static",
)

templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)


# ============================================================
# Request Models
# ============================================================

class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=30000
    )


class QARequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=10000
    )


class ExplainRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=1,
        max_length=10000
    )


class QuizRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=30000
    )


class LearningPathRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=1,
        max_length=5000
    )

    level: Literal[
        "beginner",
        "intermediate",
        "advanced"
    ] = "beginner"


# ============================================================
# Home Page
# ============================================================

@app.get(
    "/",
    response_class=HTMLResponse
)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title": "EduGenie"
        }
    )


# ============================================================
# Health Check
# ============================================================

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "service": "EduGenie"
    }


# ============================================================
# Q&A
# Endpoint: POST /qa
# ============================================================

@app.post("/qa")
async def qa(
    payload: QARequest
):

    try:

        answer = answer_question(
            payload.question
        )

        return {
            "answer": answer
        }

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc)
        ) from exc


# ============================================================
# Concept Explanation
# Endpoint: POST /explain
# ============================================================

@app.post("/explain")
async def explain(
    payload: ExplainRequest
):

    try:

        explanation = explain_concept(
            payload.topic
        )

        return {
            "explanation": explanation
        }

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc)
        ) from exc


# ============================================================
# Quiz Generation
# Endpoint: POST /quiz
# ============================================================

@app.post("/quiz")
async def quiz(
    payload: QuizRequest
):

    try:

        quiz_data = generate_quiz(
            payload.text
        )

        return {
            "quiz": quiz_data
        }

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc)
        ) from exc


# ============================================================
# Text Summarization
# Endpoint: POST /summarize
# ============================================================

@app.post("/summarize")
async def summarize(
    payload: TextRequest
):

    try:

        summary = summarize_text(
            payload.text
        )

        return {
            "summary": summary
        }

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc)
        ) from exc


# ============================================================
# Learning Recommendations
# Endpoint: POST /learn/recommendations
# ============================================================

@app.post(
    "/learn/recommendations"
)
async def learning_recommendations(
    payload: LearningPathRequest
):

    try:

        recommendations = (
            get_learning_recommendations(
                payload.topic,
                payload.level
            )
        )

        return {
            "recommendations":
                recommendations
        }

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc)
        ) from exc
