from fastapi import FastAPI, File, Form, HTTPException, UploadFile

from app.schemas.analysis_schema import AnalyzeRequest
from app.services.file_parser_service import extract_resume_text
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


@app.post("/analyze-file")
async def analyze_resume_file(
    resume_file: UploadFile = File(...),
    jd_text: str = Form(...),
    mode: str = Form(...),
):
    try:
        if mode not in ["recruiter", "job_seeker"]:
            raise HTTPException(
                status_code=400,
                detail="Invalid mode. Choose either 'recruiter' or 'job_seeker'.",
            )

        file_bytes = await resume_file.read()

        resume_text = extract_resume_text(
            file_bytes=file_bytes,
            filename=resume_file.filename,
        )

        if not resume_text or len(resume_text) < 20:
            raise HTTPException(
                status_code=400,
                detail="Could not extract enough text from the uploaded resume.",
            )

        match_result = analyze_resume_against_jd(
            resume_text=resume_text,
            jd_text=jd_text,
        )

        report = generate_report(
            match_result=match_result,
            mode=mode,
        )

        return {
            "filename": resume_file.filename,
            "extracted_text_preview": resume_text[:300],
            "report": report,
        }

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))