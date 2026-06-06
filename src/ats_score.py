from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_ats_score(resume_text, target_role):
    job_profile = f"""
    Required skills and responsibilities for the role of {target_role}.
    The candidate should have relevant skills, projects, experience,
    technical knowledge, problem-solving ability, communication skills,
    and practical understanding of the role.
    """

    documents = [resume_text, job_profile]

    vectorizer = CountVectorizer().fit_transform(documents)
    similarity = cosine_similarity(vectorizer)

    score = similarity[0][1] * 100

    return round(score, 2)