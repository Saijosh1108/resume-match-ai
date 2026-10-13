
from src.recommendations import generate_recommendations


def test_recommendations_are_returned():
    recommendations = generate_recommendations(
        ["Python", "RAG"],
        ["Python", "RAG", "FastAPI"],
        ["FastAPI"],
    )

    assert len(recommendations) > 0


def test_missing_skill_is_mentioned():
    recommendations = generate_recommendations(
        ["Python"],
        ["Python", "FastAPI"],
        ["FastAPI"],
    )

    assert any(
        "FastAPI" in recommendation
        for recommendation in recommendations
    )


def test_no_missing_skills():
    recommendations = generate_recommendations(
        ["Python", "RAG"],
        ["Python", "RAG"],
        [],
    )

    assert len(recommendations) > 0


def test_empty_job_skills():
    recommendations = generate_recommendations(
        [],
        [],
        [],
    )

    assert isinstance(recommendations, list)
