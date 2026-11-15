from app.integrations.gemini_reel import GeminiReelAnalysis, _normalize_xai_analysis


def test_xai_response_normalizes_descriptive_categories_and_limitations() -> None:
    raw = {
        "summary": "The opening needs a clearer promise.",
        "findings": [
            {
                "timestamp_seconds": 0,
                "focus": "Hook promise",
                "severity": "high",
                "observation": "The topic is not introduced immediately.",
                "recommendation": "State the result before the setup.",
            },
            {
                "timestamp_seconds": 4,
                "focus": "Caption readability",
                "severity": "moderate",
                "observation": "The caption is small.",
                "recommendation": "Increase contrast and size.",
            },
        ],
        "limitations": "Review is based only on selected strategic stills.",
    }

    normalized = _normalize_xai_analysis(raw, duration_seconds=15)
    analysis = GeminiReelAnalysis.model_validate(normalized)

    assert [finding.focus for finding in analysis.findings] == ["hook", "on_screen_text"]
    assert [finding.severity for finding in analysis.findings] == ["high", "medium"]
    assert analysis.limitations == ["Review is based only on selected strategic stills."]
