from typing import Dict, List


def generate_risk_flags(missing_skills: List[str], match_score: int) -> List[str]:
    """
    Generates recruiter-friendly risk flags based on missing skills and score.
    """
    risk_flags = []

    if match_score < 50:
        risk_flags.append("Candidate has a low match score for the current job requirements.")

    for skill in missing_skills:
        risk_flags.append(f"{skill} is not visible in the resume.")

    if not risk_flags:
        risk_flags.append("No major requirement gaps detected from the resume text.")

    return risk_flags


def generate_technical_follow_up_points(
    matched_skills: List[str],
    missing_skills: List[str],
) -> List[str]:
    """
    Generates handoff points for the hiring manager or technical interviewer.
    These are not interview questions, but areas to validate.
    """
    follow_up_points = []

    for skill in matched_skills[:3]:
        follow_up_points.append(f"Validate depth of hands-on experience with {skill}.")

    for skill in missing_skills[:2]:
        follow_up_points.append(f"Check whether {skill} is required immediately or can be learned on the job.")

    if not follow_up_points:
        follow_up_points.append("Validate the candidate's most relevant project experience.")

    return follow_up_points


def generate_recommended_next_step(match_score: int) -> str:
    """
    Suggests the next hiring workflow step.
    """
    if match_score >= 75:
        return "Move to technical screening"
    elif match_score >= 50:
        return "Keep as maybe / review manually"
    return "Do not prioritize for this role"


def generate_hiring_manager_handoff(
    decision: str,
    match_score: int,
    matched_skills: List[str],
    missing_skills: List[str],
) -> str:
    """
    Creates a concise note recruiter can share with hiring manager.
    """
    matched_text = ", ".join(matched_skills) if matched_skills else "no major matched skills"
    missing_text = ", ".join(missing_skills) if missing_skills else "no major missing skills"

    return (
        f"Candidate is marked as {decision} with a match score of {match_score}%. "
        f"Strong visible matches: {matched_text}. "
        f"Missing or unclear requirements: {missing_text}. "
        f"Recommended action: {generate_recommended_next_step(match_score)}."
    )


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
    Focuses on shortlist decision, risks, and hiring-manager handoff.
    """
    matched_skills = match_result.get("matched_skills", [])
    missing_skills = match_result.get("missing_skills", [])
    match_score = match_result.get("match_score", 0)
    decision = match_result.get("decision")

    return {
        "mode": "recruiter",
        "decision": decision,
        "match_score": match_score,
        "shortlist_reason": match_result.get("explanation"),
        "matched_requirements": matched_skills,
        "missing_requirements": missing_skills,
        "risk_flags": generate_risk_flags(
            missing_skills=missing_skills,
            match_score=match_score,
        ),
        "technical_follow_up_points": generate_technical_follow_up_points(
            matched_skills=matched_skills,
            missing_skills=missing_skills,
        ),
        "hiring_manager_handoff": generate_hiring_manager_handoff(
            decision=decision,
            match_score=match_score,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
        ),
        "recommended_next_step": generate_recommended_next_step(match_score),
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