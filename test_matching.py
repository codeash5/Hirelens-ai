from pprint import pprint

from app.services.matching_service import analyze_resume_against_jd
from app.services.report_service import generate_report


resume_text = """
Ashwini has built backend projects using Python, FastAPI, PostgreSQL,
SQLAlchemy, JWT authentication, REST APIs, GitHub, and Postman.
"""

jd_text = """
We are hiring a Python Backend Developer with FastAPI, PostgreSQL,
REST API, Docker, Redis, JWT authentication, and SQLAlchemy experience.
"""

match_result = analyze_resume_against_jd(resume_text, jd_text)

print("\n--- RAW MATCH RESULT ---")
pprint(match_result)

recruiter_report = generate_report(match_result, mode="recruiter")

print("\n--- RECRUITER REPORT ---")
pprint(recruiter_report)

job_seeker_report = generate_report(match_result, mode="job_seeker")

print("\n--- JOB SEEKER REPORT ---")
pprint(job_seeker_report)