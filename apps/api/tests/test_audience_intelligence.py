from app.services.audience_intelligence import derive_planning_personas


def test_planning_personas_are_derived_from_aggregate_segments_not_supplied_names() -> None:
    personas = derive_planning_personas(
        [
            {"field": "age_distribution", "values": {"18-24": 55, "25-34": 32}},
            {"field": "top_locations", "values": {"United States": 62, "Other": 38}},
        ],
        [{"media_type": "reel", "hashtags": ["creator", "workflow"], "keywords": ["systems"], "caption": "Build clearer creator systems"}],
    )

    assert [persona["label"] for persona in personas] == ["Systems learner · 18-24", "Systems learner · 25-34"]
    assert "55%" in personas[0]["observed_evidence"][0]
    assert "United States (62%)" in personas[0]["observed_evidence"][1]
    assert all("individual viewer" in persona["strategic_use"] for persona in personas)
    assert personas[0]["feedback_lens"] != personas[1]["feedback_lens"]
