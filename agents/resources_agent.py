from src.llm_client import ask_gemini


def recommend_learning_resources(resume_text, target_role):
    prompt = f"""
    You are a career learning advisor.

    Target Role:
    {target_role}

    Candidate Resume:
    {resume_text}

    Recommend learning resources to help this candidate become job-ready.

    Provide the response in this format:

    1. Skills to Learn First
    2. Recommended Courses
    3. Recommended Certifications
    4. Recommended YouTube Channels
    5. Recommended Books
    6. Practice Platforms
    7. 30-Day Learning Plan

    Keep it practical and beginner-friendly.
    """

    return ask_gemini(prompt)