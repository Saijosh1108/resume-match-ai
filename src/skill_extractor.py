

import re


# Canonical skill names and accepted variations
SKILL_ALIASES = {
    # Programming languages
    "Python": ["python"],
    "SQL": ["sql", "structured query language"],
    "Java": ["java"],
    "C++": ["c++"],
    "C": ["c programming", "c language"],
    "C#": ["c#", "c sharp"],
    "JavaScript": ["javascript", "js"],
    "TypeScript": ["typescript"],
    "R": ["r programming", "r language"],
    "Go": ["golang"],
    "PHP": ["php"],
    "Bash": ["bash", "shell scripting"],

    # AI and machine learning
    "Artificial Intelligence": ["artificial intelligence"],
    "Machine Learning": ["machine learning", "ml"],
    "Deep Learning": ["deep learning"],
    "NLP": ["nlp", "natural language processing"],
    "Computer Vision": ["computer vision"],
    "PyTorch": ["pytorch", "torch"],
    "TensorFlow": ["tensorflow"],
    "Scikit-learn": ["scikit-learn", "sklearn"],
    "Hugging Face": ["hugging face"],
    "Transformers": ["transformers"],
    "LLM": [
        "llm", "llms",
        "large language model", "large language models"
    ],
    "Generative AI": ["generative ai", "gen ai"],
    "RAG": [
        "rag",
        "retrieval augmented generation",
        "retrieval-augmented generation"
    ],
    "FAISS": ["faiss"],
    "Vector Database": [
        "vector database", "vector databases",
        "vector db", "vector dbs"
    ],
    "Semantic Search": ["semantic search"],
    "Prompt Engineering": ["prompt engineering"],
    "LangChain": ["langchain"],
    "LlamaIndex": ["llamaindex", "llama index"],
    "MLflow": ["mlflow"],
    "Weights & Biases": ["weights & biases", "wandb"],

    # Data analysis and visualization
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Excel": ["excel", "microsoft excel"],
    "Power BI": ["power bi", "powerbi"],
    "Tableau": ["tableau"],
    "Matplotlib": ["matplotlib"],
    "Seaborn": ["seaborn"],
    "Statistics": ["statistics", "statistical analysis"],
    "Data Visualization": ["data visualization"],
    "Data Analysis": ["data analysis", "data analytics"],
    "ETL": ["etl", "extract transform load"],
    "Apache Spark": ["apache spark", "pyspark"],
    "Hadoop": ["hadoop"],

    # Databases
    "MySQL": ["mysql"],
    "PostgreSQL": ["postgresql", "postgres"],
    "MongoDB": ["mongodb", "mongo db"],
    "SQLite": ["sqlite"],
    "Redis": ["redis"],
    "Elasticsearch": ["elasticsearch"],

    # Web development and APIs
    "HTML": ["html"],
    "CSS": ["css"],
    "React": ["react", "react.js", "reactjs"],
    "Node.js": ["node.js", "nodejs"],
    "FastAPI": ["fastapi"],
    "Flask": ["flask"],
    "Django": ["django"],
    "REST API": [
        "rest api", "rest apis",
        "restful api", "restful apis"
    ],
    "GraphQL": ["graphql"],

    # Cloud and DevOps
    "Docker": ["docker"],
    "Kubernetes": ["kubernetes", "k8s"],
    "AWS": ["aws", "amazon web services"],
    "Azure": ["azure", "microsoft azure"],
    "GCP": ["gcp", "google cloud platform"],
    "Git": ["git"],
    "GitHub": ["github"],
    "Linux": ["linux"],
    "CI/CD": ["ci/cd", "continuous integration", "continuous delivery"],
    "Terraform": ["terraform"],
    "Jenkins": ["jenkins"],

    # Business and project tools
    "Jira": ["jira"],
    "Confluence": ["confluence"],
    "Agile": ["agile"],
    "Scrum": ["scrum"],
    "Project Management": ["project management"],
    "Communication": ["communication skills"],
}


def contains_term(text, term):
    """Match a term without matching it inside unrelated words."""
    pattern = r"(?<!\w)" + re.escape(term) + r"(?!\w)"
    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def extract_skills(text):
    """Return unique, normalized skills detected in the text."""
    found_skills = set()

    for canonical_name, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            if contains_term(text, alias):
                found_skills.add(canonical_name)
                break

    return sorted(found_skills)
