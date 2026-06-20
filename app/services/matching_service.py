from typing import Dict, List


COMMON_TECH_SKILLS = [
    "python",
    "fastapi",
    "flask",
    "django",
    "sql",
    "postgresql",
    "mysql",
    "mongodb",
    "sqlalchemy",
    "pydantic",
    "rest api",
    "jwt",
    "authentication",
    "docker",
    "redis",
    "celery",
    "aws",
    "git",
    "github",
    "postman",
    "pytest",
    "html",
    "css",
    "javascript",
    "react",
    "node.js",
    "express",
    "machine learning",
    "nlp",
    "pandas",
    "numpy",
]


def extract_skills(text: str) -> List[str]:
    """
    Extracts known technical skills from a block of text.
    This is a simple v1 skill extractor using keyword matching.
    """
    text_lower = text.lower()

    found_skills = []

    for skill in COMMON_TECH_SKILLS:
        if skill in text_lower:
            found_skills.append(skill)

    return found_skills


def decide_candidate(match_score: int) -> str:
    """
    Converts numeric score into a recruiter-friendly decision.
    """
    if match_score >= 75:
        return "Shortlist"
    elif match_score >= 50:
        return "Maybe"
    return "Not Recommended"


def generate_explanation(
    matched_skills: List[str],
    missing_skills: List[str],
    match_score: int,
) -> str:
    """
    Generates a simple explanation for why the candidate received this score.
    """
    if match_score >= 75:
        strength = "The candidate is a strong fit for this role."
    elif match_score >= 50:
        strength = "The candidate is a partial fit for this role."
    else:
        strength = "The candidate does not strongly match the role requirements yet."

    matched_text = ", ".join(matched_skills) if matched_skills else "no major matching skills"
    missing_text = ", ".join(missing_skills) if missing_skills else "no major missing skills"

    return (
        f"{strength} Matched skills include: {matched_text}. "
        f"Missing or weak skills include: {missing_text}."
    )


def analyze_resume_against_jd(resume_text: str, jd_text: str) -> Dict:
    """
    Compares resume text with job description text.

    Returns:
    - match_score
    - matched_skills
    - missing_skills
    - decision
    - explanation
    """
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    if not jd_skills:
        return {
            "match_score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "decision": "Cannot Analyze",
            "explanation": "No recognizable technical skills were found in the job description.",
        }

    matched_skills = [skill for skill in jd_skills if skill in resume_skills]
    missing_skills = [skill for skill in jd_skills if skill not in resume_skills]

    match_score = round((len(matched_skills) / len(jd_skills)) * 100)

    decision = decide_candidate(match_score)

    explanation = generate_explanation(
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        match_score=match_score,
    )

    return {
        "match_score": match_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "decision": decision,
        "explanation": explanation,
    }