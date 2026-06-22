from typing import Dict, List, Tuple

from app.services.matching_service import extract_skills


MUST_HAVE_HEADINGS = [
    "required skills",
    "requirements",
    "must have",
    "must-have",
    "mandatory skills",
    "essential skills",
    "primary skills",
    "core skills",
]

GOOD_TO_HAVE_HEADINGS = [
    "good to have",
    "good-to-have",
    "nice to have",
    "nice-to-have",
    "preferred skills",
    "preferred",
    "bonus",
    "plus",
    "optional",
]

DEFAULT_BACKEND_MUST_HAVE = [
    "python",
    "fastapi",
    "django",
    "flask",
    "rest api",
    "sql",
    "postgresql",
    "mysql",
    "sqlalchemy",
    "jwt",
    "authentication",
]


def find_heading_type(line: str) -> str:
    """
    Detects whether a line is a must-have or good-to-have section heading.
    """
    line_lower = line.lower().strip().replace(":", "")

    if any(heading in line_lower for heading in MUST_HAVE_HEADINGS):
        return "must_have"

    if any(heading in line_lower for heading in GOOD_TO_HAVE_HEADINGS):
        return "good_to_have"

    return "none"


def extract_section_texts(jd_text: str) -> Tuple[str, str]:
    """
    Extracts text under must-have and good-to-have sections.
    This handles JDs like:

    Required skills:
    Python, FastAPI, Docker

    Good to have:
    AWS, Redis
    """
    must_have_text = ""
    good_to_have_text = ""

    current_section = None

    lines = jd_text.splitlines()

    for line in lines:
        clean_line = line.strip()

        if not clean_line:
            continue

        heading_type = find_heading_type(clean_line)

        if heading_type == "must_have":
            current_section = "must_have"
            continue

        if heading_type == "good_to_have":
            current_section = "good_to_have"
            continue

        if current_section == "must_have":
            must_have_text += " " + clean_line

        elif current_section == "good_to_have":
            good_to_have_text += " " + clean_line

    return must_have_text, good_to_have_text


def classify_unmarked_skill(skill: str) -> str:
    """
    Fallback classification when JD wording does not clearly mark the skill.
    """
    if skill in DEFAULT_BACKEND_MUST_HAVE:
        return "must_have"

    return "good_to_have"


def extract_requirements_from_jd(jd_text: str) -> Dict:
    """
    Extracts skills from JD and classifies them into must-have and good-to-have.

    Priority:
    1. Section headings like Required Skills / Good to Have
    2. Fallback backend assumptions if unclear
    """
    detected_skills = extract_skills(jd_text)

    must_have_section_text, good_to_have_section_text = extract_section_texts(jd_text)

    must_have_section_skills = extract_skills(must_have_section_text)
    good_to_have_section_skills = extract_skills(good_to_have_section_text)

    must_have_skills = []
    good_to_have_skills = []

    for skill in detected_skills:
        if skill in must_have_section_skills:
            must_have_skills.append(skill)
        elif skill in good_to_have_section_skills:
            good_to_have_skills.append(skill)
        else:
            fallback_classification = classify_unmarked_skill(skill)

            if fallback_classification == "must_have":
                must_have_skills.append(skill)
            else:
                good_to_have_skills.append(skill)

    return {
        "detected_skills": detected_skills,
        "must_have_skills": must_have_skills,
        "good_to_have_skills": good_to_have_skills,
        "classification_method": "section_based_with_backend_fallback",
    }