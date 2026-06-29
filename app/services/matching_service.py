import re
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

SKILL_ALIASES = {
    "python": ["python", "python programming"],
    "fastapi": ["fastapi", "fast api"],
    "flask": ["flask"],
    "django": ["django"],
    "sql": ["sql", "structured query language"],
    "postgresql": ["postgresql", "postgres", "postgre sql"],
    "mysql": ["mysql", "my sql"],
    "mongodb": ["mongodb", "mongo db"],
    "sqlalchemy": ["sqlalchemy", "sql alchemy"],
    "pydantic": ["pydantic"],
    "rest api": [
        "rest api",
        "rest apis",
        "restful api",
        "restful apis",
        "api development",
        "api design",
        "apis",
    ],
    "jwt": ["jwt", "json web token", "jwt authentication", "jwt-based authentication"],
    "authentication": ["authentication", "auth", "login system", "user authentication"],
    "docker": ["docker", "containerization", "containerisation"],
    "redis": ["redis"],
    "celery": ["celery"],
    "aws": ["aws", "amazon web services"],
    "git": ["git", "version control"],
    "github": ["github", "git hub"],
    "postman": ["postman"],
    "pytest": ["pytest", "py test"],
    "html": ["html"],
    "css": ["css"],
    "javascript": ["javascript", "js"],
    "react": ["react", "react.js", "reactjs"],
    "node.js": ["node.js", "nodejs", "node js"],
    "express": ["express", "express.js", "expressjs"],
    "machine learning": ["machine learning", "ml"],
    "nlp": ["nlp", "natural language processing"],
    "pandas": ["pandas"],
    "numpy": ["numpy", "num py"],
}

def extract_skills(text: str) -> List[str]:
    """
    Extracts known technical skills from a block of text.

    Uses canonical skill names with alias support.
    Example:
    - "REST APIs" maps to "rest api"
    - "Postgres" maps to "postgresql"
    - "Natural Language Processing" maps to "nlp"
    """
    text_lower = text.lower()

    found_skills = []

    for canonical_skill in COMMON_TECH_SKILLS:
        aliases = SKILL_ALIASES.get(canonical_skill, [canonical_skill])

        for alias in aliases:
            pattern = r"(?<![a-zA-Z0-9])" + re.escape(alias) + r"(?![a-zA-Z0-9])"

            if re.search(pattern, text_lower):
                found_skills.append(canonical_skill)
                break

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
            "scoring_method": "weighted_skill_match",
        },
    }


def calculate_weighted_skill_score(
    matched_skills: List[str],
    required_skills: List[str],
) -> float:
    """
    Calculates weighted skill coverage.

    Example:
    If required skills are Python, FastAPI, Git
    and resume has Python + Git,
    Python should matter more than Git because of SKILL_WEIGHTS.
    """
    if not required_skills:
        return 0.0

    total_weight = sum(SKILL_WEIGHTS.get(skill, 1) for skill in required_skills)
    matched_weight = sum(SKILL_WEIGHTS.get(skill, 1) for skill in matched_skills)

    if total_weight == 0:
        return 0.0

    return (matched_weight / total_weight) * 100


def analyze_resume_against_requirements(
    resume_text: str,
    must_have_skills: List[str],
    good_to_have_skills: List[str],
) -> Dict:
    """
    Compares resume text against structured job requirements.

    Scoring v2:
    - 50% weighted must-have skill coverage
    - 20% weighted good-to-have skill coverage

    Later upgrades:
    - 15% TF-IDF / semantic similarity
    - 10% evidence strength
    - 5% resume quality
    """
    resume_skills = extract_skills(resume_text)

    matched_must_have_skills = [
        skill for skill in must_have_skills if skill in resume_skills
    ]
    missing_must_have_skills = [
        skill for skill in must_have_skills if skill not in resume_skills
    ]

    matched_good_to_have_skills = [
        skill for skill in good_to_have_skills if skill in resume_skills
    ]
    missing_good_to_have_skills = [
        skill for skill in good_to_have_skills if skill not in resume_skills
    ]

    must_have_coverage = calculate_weighted_skill_score(
        matched_skills=matched_must_have_skills,
        required_skills=must_have_skills,
    )

    good_to_have_coverage = calculate_weighted_skill_score(
        matched_skills=matched_good_to_have_skills,
        required_skills=good_to_have_skills,
    )

    must_have_contribution = must_have_coverage * 0.50
    good_to_have_contribution = good_to_have_coverage * 0.20

    match_score = round(must_have_contribution + good_to_have_contribution)

    decision = decide_candidate(match_score)

    matched_skills = matched_must_have_skills + matched_good_to_have_skills
    missing_skills = missing_must_have_skills + missing_good_to_have_skills

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
        "matched_must_have_skills": matched_must_have_skills,
        "missing_must_have_skills": missing_must_have_skills,
        "matched_good_to_have_skills": matched_good_to_have_skills,
        "missing_good_to_have_skills": missing_good_to_have_skills,
        "score_breakdown": {
            "must_have_coverage": round(must_have_coverage),
            "good_to_have_coverage": round(good_to_have_coverage),
            "must_have_contribution": round(must_have_contribution, 2),
            "good_to_have_contribution": round(good_to_have_contribution, 2),
            "scoring_method": "weighted_must_have_50_good_to_have_20",
            "planned_remaining_layers": {
                "semantic_similarity": 15,
                "evidence_strength": 10,
                "resume_quality": 5,
            },
        },
    }