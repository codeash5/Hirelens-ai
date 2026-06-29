from pprint import pprint

from app.services.matching_service import analyze_resume_against_requirements


resume_text = """
Ashwini has built backend projects using Python, FastAPI, PostgreSQL,
SQLAlchemy, JWT authentication, REST APIs, GitHub, and Postman.
"""

must_have_skills = ["python", "fastapi", "docker", "redis"]
good_to_have_skills = ["postgresql", "aws"]

result = analyze_resume_against_requirements(
    resume_text=resume_text,
    must_have_skills=must_have_skills,
    good_to_have_skills=good_to_have_skills,
)

pprint(result)