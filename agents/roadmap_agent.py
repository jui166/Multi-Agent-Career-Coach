from src.llm_client import ask_gemini


def generate_roadmap(resume_text, target_role):

    prompt = f"""
    Create a 6-month learning roadmap.

    Target Role:
    {target_role}

    Resume:
    {resume_text}

    Include:

    Month 1
    Month 2
    Month 3
    Month 4
    Month 5
    Month 6

    Mention skills, courses and milestones.
    """

    return ask_gemini(prompt)