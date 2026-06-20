from pprint import pprint
from app.services.matching_service import analyze_resume_against_jd



resume_text = """
Ashwini has built backend projects using Python, FastAPI, PostgreSQL,
SQLAlchemy, JWT authentication, REST APIs, GitHub, and Postman.
"""

jd_text = """
We are hiring a Python Backend Developer with FastAPI, PostgreSQL,
REST API, Docker, Redis, JWT authentication, and SQLAlchemy experience.
"""

result = analyze_resume_against_jd(resume_text, jd_text)

print(result)