from src.llm_client import ask_gemini


def recruiter_decision(resume_text, target_role, ats_score):
    prompt = f"""
    You are a senior recruiter hiring for the role of {target_role}.

    Candidate Resume:
    {resume_text}

    ATS Score:
    {ats_score}%

    Give a professional hiring review in this format:

    1. Shortlist Decision: YES / MAYBE / NO
    2. Reason for Decision
    3. Candidate Strengths
    4. Recruiter Concerns
    5. Final Hiring Recommendation

    Keep the response clear, practical, and recruiter-like.
    """

    return ask_gemini(prompt)