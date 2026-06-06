from src.llm_client import ask_gemini


def recommend_projects(resume_text, target_role):

    prompt = f"""
    Recommend 5 impressive portfolio projects.

    Target Role:
    {target_role}

    Resume:
    {resume_text}

    For each project provide:

    - Project Name
    - Description
    - Technologies
    - Difficulty Level
    """

    return ask_gemini(prompt)