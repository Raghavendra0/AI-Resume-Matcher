# src/skill_scoring.py

from src.skill_weights import SKILL_CONFIG

def weighted_skill_breakdown(resume_text: str, job_description: str):
    resume_text = resume_text.lower()
    job_description = job_description.lower()

    matched = []
    missing = []
    category_scores = {}

    total_weight = 0
    matched_weight = 0

    for category, config in SKILL_CONFIG.items():
        weight = config["weight"]
        skills = config["skills"]

        total_weight += weight

        job_skills = [s for s in skills if s in job_description]
        resume_skills = [s for s in job_skills if s in resume_text]

        if job_skills:
            category_score = (len(resume_skills) / len(job_skills)) * weight
            matched_weight += category_score
            category_scores[category] = round(category_score, 2)
        else:
            category_scores[category] = 0

        matched.extend(resume_skills)
        missing.extend(set(job_skills) - set(resume_skills))

    final_score = round((matched_weight / total_weight) * 100, 2) if total_weight else 0.0

    return {
        "score": final_score,          # ✅ SINGLE SOURCE
        "matched": sorted(set(matched)),
        "missing": sorted(set(missing)),
        "category_scores": category_scores
    }
