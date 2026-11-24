import pytest

import src.matcher as matcher


class FakeModel:
    def encode(self, texts):
        vectors = {
            "resume": [1.0, 0.0],
            "job": [1.0, 0.0],
            "opposite": [-1.0, 0.0],
        }
        return [vectors[text] for text in texts]


def test_identical_embeddings_return_100(monkeypatch):
    monkeypatch.setattr(matcher, "_load_model", lambda: FakeModel())

    assert matcher.calculate_similarity("resume", "job") == 100.0


def test_negative_similarity_is_clamped_to_zero(monkeypatch):
    monkeypatch.setattr(matcher, "_load_model", lambda: FakeModel())

    assert matcher.calculate_similarity("resume", "opposite") == 0.0


@pytest.mark.parametrize(
    ("resume_text", "job_description"),
    [
        ("", "Python developer"),
        ("   ", "Python developer"),
        ("Resume text", ""),
        ("Resume text", "  "),
    ],
)
def test_empty_inputs_raise_clear_error(resume_text, job_description):
    with pytest.raises(ValueError):
        matcher.calculate_similarity(resume_text, job_description)
