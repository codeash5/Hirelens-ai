from fastapi import FastAPI

from app.schemas.analysis_schema import AnalyzeRequest
from app.services.matching_service import analyze_resume_against_jd
from app.services.report_service import generate_report


app = FastAPI(
    title="HireLens AI",
    description="Dual-mode AI resume screening and job fit analysis API",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "Welcome to HireLens AI",
        "status": "running",
    }


@app.post("/analyze")
def analyze_resume(request: AnalyzeRequest):
    match_result = analyze_resume_against_jd(
        resume_text=request.resume_text,
        jd_text=request.jd_text,
    )

    report = generate_report(
        match_result=match_result,
        mode=request.mode,
    )

    return report