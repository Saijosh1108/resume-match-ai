
def generate_recommendations(
    resume_skills,
    job_skills,
    missing_skills,
):
    """
    Generate rule-based resume improvement suggestions.
    Suggestions are based on detected skill gaps.
    """

    recommendations = []

    # Overall skill coverage
    if job_skills:
        matched_skills = set(resume_skills) & set(job_skills)

        coverage = round(
            len(matched_skills) / len(job_skills) * 100,
            2,
        )

        if coverage < 50:
            recommendations.append(
                "Your resume currently covers fewer than half "
                "of the recognized job skills. Review the job "
                "requirements and highlight relevant experience "
                "you genuinely have."
            )

        elif coverage < 80:
            recommendations.append(
                "Your resume covers several recognized job skills. "
                "Strengthen the sections describing your projects "
                "and experience to demonstrate how you used them."
            )

        else:
            recommendations.append(
                "Your resume covers most of the recognized job skills. "
                "Focus on demonstrating your depth of experience "
                "with concrete project examples and results."
            )

    # Skill-specific recommendations
    if missing_skills:
        recommendations.append(
            "Review these skills not detected in your resume: "
            + ", ".join(sorted(missing_skills))
            + ". If you have relevant experience with any of them, "
            "consider adding it clearly to your resume."
        )

    # Project advice
    if any(
        skill in set(job_skills)
        for skill in ["Machine Learning", "Deep Learning", "NLP", "LLM", "RAG"]
    ):
        recommendations.append(
            "For relevant AI projects, explain the problem, "
            "your technical approach, the tools you used, "
            "and measurable results where available."
        )

    # Resume writing advice
    recommendations.append(
        "Use concise bullet points that begin with action verbs. "
        "Describe your own contribution and include measurable "
        "results only when you can substantiate them."
    )

    return recommendations
