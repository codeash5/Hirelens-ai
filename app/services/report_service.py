from typing import Dict, List


def generate_interview_questions(missing_skills: List[str], matched_skills: List[str]) -> List[str]:
    """
    Generates recruiter-focused interview questions based on matched and missing skills.
    """
    questions = []

    for skill in matched_skills[:3]:
        questions.append(f"Can you explain your hands-on experience with {skill}?")

    for skill in missing_skills[:2]:
        questions.append(f"How would you approach learning or using {skill} in this role?")

    if not questions:
        questions.append("Can you walk me through your most relevant project for this role?")

    return questions


def generate_improvement_advice(missing_skills: List[str]) -> List[str]:
    """
    Generates job seeker-focused improvement advice based on missing skills.
    """
    if not missing_skills:
        return ["Your resume already covers the major detected job requirements. Improve by adding stronger project impact and measurable results."]

    advice = []

    for skill in missing_skills:
        advice.append(f"Add or strengthen proof of {skill} through a project, bullet point, or certification.")

    return advice


def generate_resume_bullet_suggestions(matched_skills: List[str], missing_skills: List[str]) -> List[str]:
    """
    Generates sample resume bullet suggestions for job seekers.
    """
    bullets = []

    if matched_skills:
        skill_text = ", ".join(matched_skills[:5])
        bullets.append(
            f"Built backend features using {skill_text}, focusing on API design, database integration, and clean service-layer logic."
        )

    if missing_skills:
        missing_text = ", ".join(missing_skills[:3])
        bullets.append(
            f"Planned project upgrades to include {missing_text}, improving production readiness and backend system depth."
        )

    return bullets


def build_recruiter_report(match_result: Dict) -> Dict:
    """
    Formats matching result for recruiter mode.
    """
    matched_skills = match_result.get("matched_skills", [])
    missing_skills = match_result.get("missing_skills", [])

    return {
        "mode": "recruiter",
        "decision": match_result.get("decision"),
        "match_score": match_result.get("match_score"),
        "recruiter_summary": match_result.get("explanation"),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "interview_questions": generate_interview_questions(
            missing_skills=missing_skills,
            matched_skills=matched_skills,
        ),
        "score_breakdown": match_result.get("score_breakdown"),
    }


def build_job_seeker_report(match_result: Dict) -> Dict:
    """
    Formats matching result for job seeker mode.
    """
    matched_skills = match_result.get("matched_skills", [])
    missing_skills = match_result.get("missing_skills", [])
    match_score = match_result.get("match_score", 0)

    if match_score >= 75:
        readiness = "Strong fit"
    elif match_score >= 50:
        readiness = "Partial fit"
    else:
        readiness = "Needs improvement"

    return {
        "mode": "job_seeker",
        "readiness": readiness,
        "match_score": match_score,
        "summary": match_result.get("explanation"),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "improvement_advice": generate_improvement_advice(missing_skills),
        "resume_bullet_suggestions": generate_resume_bullet_suggestions(
            matched_skills=matched_skills,
            missing_skills=missing_skills,
        ),
        "score_breakdown": match_result.get("score_breakdown"),
    }


def generate_report(match_result: Dict, mode: str) -> Dict:
    """
    Main report function.
    Converts raw matching result into recruiter or job seeker report.
    """
    if mode == "recruiter":
        return build_recruiter_report(match_result)

    if mode == "job_seeker":
        return build_job_seeker_report(match_result)

    raise ValueError("Invalid mode. Choose either 'recruiter' or 'job_seeker'.")