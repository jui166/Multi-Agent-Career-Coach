from src.llm_client import ask_gemini


def analyze_resume(resume_text, target_role):

    prompt = f"""
    You are an expert career coach.

    Analyze the following resume for the role of:
    {target_role}

    Resume:
    {resume_text}

    Provide:

    1. Strengths
    2. Weaknesses
    3. Overall evaluation
    """

    return ask_gemini(prompt)