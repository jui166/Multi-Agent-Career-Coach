from src.llm_client import ask_gemini


def generate_interview_questions(resume_text, target_role):

    prompt = f"""
    Generate interview questions for:

    {target_role}

    Based on:

    {resume_text}

    Include:

    - Technical Questions
    - Behavioral Questions
    - Project Questions
    """

    return ask_gemini(prompt)