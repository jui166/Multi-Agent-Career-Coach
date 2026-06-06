from src.llm_client import ask_gemini


def identify_skill_gaps(resume_text, target_role):

    prompt = f"""
    Compare this resume against a typical {target_role} job profile.

    Resume:
    {resume_text}

    Identify:

    1. Missing technical skills
    2. Missing soft skills
    3. Certifications recommended
    4. Priority skills to learn
    """

    return ask_gemini(prompt)