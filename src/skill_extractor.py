
import re


# Canonical skill names and their accepted variations
SKILL_ALIASES = {
    "Python": ["python"],
    "SQL": ["sql", "structured query language"],
    "Java": ["java"],
    "C++": ["c++"],
    "JavaScript": ["javascript"],
    "Machine Learning": ["machine learning", "ml"],
    "Deep Learning": ["deep learning"],
    "NLP": ["nlp", "natural language processing"],
    "Computer Vision": ["computer vision"],
    "Artificial Intelligence": [
        "artificial intelligence",
        "ai"
    ],
    "PyTorch": ["pytorch", "torch"],
    "TensorFlow": ["tensorflow"],
    "Scikit-learn": ["scikit-learn", "sklearn"],
    "Hugging Face": ["hugging face"],
    "Transformers": ["transformers"],
    "LLM": ["llm", "llms", "large language model",
            "large language models"],
    "Generative AI": ["generative ai", "gen ai"],
    "RAG": [
        "rag",
        "retrieval augmented generation",
        "retrieval-augmented generation"
    ],
    "FAISS": ["faiss"],
    "Vector Database": [
        "vector database",
        "vector databases",
        "vector db",
        "vector dbs"
    ],
    "Semantic Search": ["semantic search"],
    "FastAPI": ["fastapi"],
    "REST API": ["rest api", "rest apis", "restful api",
                 "restful apis"],
    "Docker": ["docker"],
    "Kubernetes": ["kubernetes", "k8s"],
    "AWS": ["aws", "amazon web services"],
    "Azure": ["azure", "microsoft azure"],
    "GCP": ["gcp", "google cloud platform"],
    "Git": ["git"],
    "GitHub": ["github"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Spark": ["spark", "apache spark"],
    "Bash": ["bash"],
    "Linux": ["linux"],
}


def contains_term(text, term):
    """
    Match a term without matching it inside unrelated words.
    """
    pattern = r"(?<!\w)" + re.escape(term) + r"(?!\w)"
    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def extract_skills(text):
    """
    Return unique, normalized skills detected in the text.
    """
    found_skills = set()

    for canonical_name, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            if contains_term(text, alias):
                found_skills.add(canonical_name)
                break

    return sorted(found_skills)
