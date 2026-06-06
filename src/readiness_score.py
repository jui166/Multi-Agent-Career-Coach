def calculate_readiness_score(
    ats_score,
    num_projects,
    num_skills
):

    ats_component = min(ats_score, 100) * 0.5

    project_component = min(num_projects * 10, 25)

    skill_component = min(num_skills * 2.5, 25)

    final_score = (
        ats_component +
        project_component +
        skill_component
    )

    return round(min(final_score, 100), 2)
def readiness_status(score):

    if score >= 90:
        return "🟢 Job Ready"

    elif score >= 75:
        return "🟡 Almost Ready"

    else:
        return "🔴 Needs Improvement"