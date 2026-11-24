from src.skill_extractor import extract_skills


def test_extracts_and_normalizes_common_ai_skills():
    skills = extract_skills(
        "Python, SQL, machine learning, PyTorch, and retrieval-augmented generation"
    )

    assert skills == sorted(
        ["Python", "SQL", "Machine Learning", "PyTorch", "RAG"]
    )


def test_javascript_does_not_create_java_false_positive():
    skills = extract_skills("The frontend uses JavaScript.")

    assert "JavaScript" in skills
    assert "Java" not in skills


def test_empty_text_returns_empty_list():
    assert extract_skills("") == []
