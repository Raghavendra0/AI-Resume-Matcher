def resume_recommendations(missing_skills):
    """
    Generate actionable resume improvement suggestions
    based on missing skills.
    """

    suggestions = []

    if not missing_skills:
        return ["Your resume already covers the major required skills."]

    for skill in missing_skills:
        suggestions.append(
            f"Add hands-on experience with **{skill}** by building a small project, "
            f"adding coursework, or mentioning practical usage in your resume."
        )

    return suggestions
