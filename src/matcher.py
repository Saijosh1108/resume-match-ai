from functools import lru_cache
import math

from sklearn.metrics.pairwise import cosine_similarity


@lru_cache(maxsize=1)
def _load_model():
    """Load the embedding model only when a comparison is requested."""
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer("all-MiniLM-L6-v2")


def calculate_similarity(resume_text, job_description):
    """Return a 0-100 semantic similarity score for two non-empty texts."""
    if not isinstance(resume_text, str) or not resume_text.strip():
        raise ValueError("Resume text is empty. Please upload a readable resume.")

    if not isinstance(job_description, str) or not job_description.strip():
        raise ValueError("Job description is empty. Please provide a job description.")

    model = _load_model()
    embeddings = model.encode([resume_text, job_description])
    similarity = float(cosine_similarity([embeddings[0]], [embeddings[1]])[0][0])

    if not math.isfinite(similarity):
        raise ValueError("Could not calculate a valid semantic similarity score.")

    # Negative cosine similarity is treated as zero for this displayed score.
    score = max(0.0, min(100.0, similarity * 100))
    return round(score, 2)
