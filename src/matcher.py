from src.pdf_parser import extract_text_from_pdf
from src.skill_scoring import weighted_skill_breakdown

def match_resume_job(resume_text, job_description):
    breakdown = weighted_skill_breakdown(resume_text, job_description)

    score = breakdown["score"]

    if score >= 70:
        fit_label = "Good Fit"
        recommendation = "You are a strong match for this role."
    elif score >= 40:
        fit_label = "Partial Fit"
        recommendation = "You meet some requirements but upskilling is advised."
    else:
        fit_label = "Poor Fit"
        recommendation = "Significant upskilling is recommended."

    return {
        "match_percentage": score,
        "fit_label": fit_label,
        "recommendation": recommendation,
        "matched_skills": breakdown["matched"],
        "missing_skills": breakdown["missing"],
        "category_scores": breakdown["category_scores"],
        "skill_match_percentage": score
    }
