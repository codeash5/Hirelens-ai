from pprint import pprint

from app.services.requirement_service import extract_requirements_from_jd


jd_text = """
We are hiring a Backend Engineer.

Required skills:
Python, FastAPI, Docker, Redis

Good to have:
AWS, PostgreSQL
"""

result = extract_requirements_from_jd(jd_text)

pprint(result)