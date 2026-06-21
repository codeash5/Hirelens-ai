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

SKILL_WEIGHTS = {
    "python": 10,
    "fastapi": 10,
    "flask": 7,
    "django": 8,
    "sql": 8,
    "postgresql": 8,
    "mysql": 7,
    "mongodb": 7,
    "sqlalchemy": 7,
    "pydantic": 6,
    "rest api": 8,
    "jwt": 6,
    "authentication": 6,
    "docker": 5,
    "redis": 5,
    "celery": 5,
    "aws": 5,
    "git": 3,
    "github": 3,
    "postman": 3,
    "pytest": 4,
    "html": 2,
    "css": 2,
    "javascript": 5,
    "react": 5,
    "node.js": 7,
    "express": 7,
    "machine learning": 6,
    "nlp": 6,
    "pandas": 5,
    "numpy": 5,
}

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

    total_weight = sum(SKILL_WEIGHTS.get(skill, 1) for skill in jd_skills)
    matched_weight = sum(SKILL_WEIGHTS.get(skill, 1) for skill in matched_skills)

    match_score = round((matched_weight / total_weight) * 100)
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
    "score_breakdown": {
        "total_jd_skill_weight": total_weight,
        "matched_skill_weight": matched_weight,
        "scoring_method": "weighted_skill_match"
    }
}