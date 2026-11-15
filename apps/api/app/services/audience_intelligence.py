"""Deterministic, provenance-aware audience planning synthesis.

This service is shared by every ingestion source. It deliberately derives only
repeatable observations and hypotheses from stored aggregate evidence and
creator-owned media; it never uses fixture personas, recommendation fixtures,
or interest-score labels.
"""

from collections import Counter
import re


def _media_keywords(media: list[dict]) -> list[str]:
    supplied = [
        str(keyword).strip().lower()
        for item in media
        for keyword in item.get("keywords", [])
        if isinstance(keyword, str) and keyword.strip()
    ]
    caption_words = [
        token.lower()
        for item in media
        for token in re.findall(r"\b[a-zA-Z][a-zA-Z0-9]{3,}\b", item.get("caption", ""))
        if token.lower() not in {"about", "after", "and", "from", "have", "into", "just", "later", "that", "the", "this", "three", "tips", "with", "your"}
    ]
    return [term for term, _ in Counter([*supplied, *caption_words]).most_common(4)]


def _top_terms(media: list[dict]) -> list[str]:
    tags = [
        str(tag).removeprefix("#").strip().lower()
        for item in media
        for tag in item.get("hashtags", [])
        if isinstance(tag, str) and tag.strip()
    ]
    return [term for term, _ in Counter(tags).most_common(3)] or _media_keywords(media)[:3]


def _high_signal_keywords(media: list[dict]) -> list[str]:
    """Rank only creator-supplied terms by a bounded observed engagement weight."""
    scores: Counter[str] = Counter()
    for item in media:
        metrics = item.get("observed_metrics") if isinstance(item.get("observed_metrics"), dict) else {}
        weight = 1 + float(metrics.get("likes", 0)) + (4 * float(metrics.get("comments", 0)))
        weight += (4 * float(metrics.get("saves", 0))) + (5 * float(metrics.get("shares", 0)))
        for keyword in item.get("keywords", []):
            if isinstance(keyword, str) and keyword.strip():
                scores[keyword.strip().lower()] += weight
    return [term for term, _ in scores.most_common(6)] or _media_keywords(media)


def _pretty_term(term: str) -> str:
    return re.sub(r"[_-]+", " ", term).strip().title()


def derive_audience_hypotheses(aggregates: list[dict], media: list[dict]) -> dict[str, list[str] | str]:
    """Return evidence-grounded planning hypotheses, never individual claims."""
    formats = Counter(str(item.get("media_type", "post")) for item in media)
    terms = _top_terms(media)
    keywords = _media_keywords(media)
    top_format = formats.most_common(1)[0][0] if formats else None
    top_term = terms[0] if terms else None
    observed_fields = {str(item.get("field")) for item in aggregates}

    preferences: list[str] = []
    if top_format:
        preferences.append(
            f"Hypothesis: test another {top_format} built around the creator's recurring format before changing several variables at once."
        )
    if terms:
        preferences.append(
            f"Hypothesis: compare angles around {', '.join(f'#{term}' for term in terms[:2])}; these are recurring creator-history terms, not proven audience interests."
        )
    if "age_distribution" in observed_fields or "top_locations" in observed_fields:
        preferences.append(
            "Hypothesis: use the available aggregate age and location context to test clearer phrasing and posting windows; it does not establish any individual viewer preference."
        )

    hooks = [
        f'Hypothesis to test: open with the concrete value or outcome for “{top_term}” in the first line.'
        if top_term else "Hypothesis to test: make the first line state a concrete value before the setup."
    ]
    pacing = [
        "Hypothesis: keep the first value beat early, then test one clear visual or topic change rather than assuming a retention pattern."
    ]
    ctas = [
        f"Hypothesis: test one low-friction CTA tied to {keywords[0]!r}, then compare later observed outcomes."
        if keywords else "Hypothesis: test one low-friction save, comment, or follow CTA and compare later observed outcomes."
    ]
    motivations = [
        f"Hypothesis: the creator's repeated {keyword!r} language may be useful context for a future content test."
        for keyword in keywords[:3]
    ]
    interests = [
        f"Hypothesis: {term!r} is a recurring creator-history topic worth testing, not a verified audience preference."
        for term in terms[:3]
    ]
    return {
        "inferred_interests": interests,
        "likely_motivations": motivations,
        "content_preferences": preferences,
        "suggested_hooks": hooks,
        "pacing_considerations": pacing,
        "cta_preferences": ctas,
    }


def _ranked_values(aggregates: list[dict], field: str, *, exclude_other: bool = False) -> list[tuple[str, float]]:
    """Return only numeric aggregate values, retaining source data without extrapolation."""
    values: list[tuple[str, float]] = []
    for aggregate in aggregates:
        if aggregate.get("field") != field or not isinstance(aggregate.get("values"), dict):
            continue
        for label, value in aggregate["values"].items():
            if not isinstance(value, (int, float)) or value < 0:
                continue
            if exclude_other and str(label).strip().lower() in {"other", "other_or_unspecified"}:
                continue
            values.append((str(label), float(value)))
    return sorted(values, key=lambda item: (-item[1], item[0]))


def derive_planning_personas(aggregates: list[dict], media: list[dict]) -> list[dict]:
    """Create repeatable planning personas from actual stored aggregates and history.

    These are not demographic stereotypes or individual audience profiles. Each
    lens identifies an aggregate segment and attaches only the same creator-
    history hypotheses available to every segment.
    """
    hypotheses = derive_audience_hypotheses(aggregates, media)
    age_segments = _ranked_values(aggregates, "age_distribution")[:2]
    locations = _ranked_values(aggregates, "top_locations", exclude_other=True)[:1]
    terms = _top_terms(media)
    high_signal_terms = _high_signal_keywords(media)
    personas: list[dict] = []

    for index, (age_band, share) in enumerate(age_segments):
        theme_terms = high_signal_terms[index * 2:index * 2 + 2] or high_signal_terms[:2] or terms[:2]
        theme = " + ".join(_pretty_term(term) for term in theme_terms) or "creator-history"
        if index == 0:
            feedback_lens = f"Hypothesis to test: make the {theme} payoff visible immediately, then give one concrete next step."
            simulated_need = f"Hypothesis: this {age_band} aggregate segment may respond to a quick, concrete {theme} outcome; validate with later observed results."
        else:
            feedback_lens = f"Hypothesis to test: state the {theme} result first, then show one practical proof before the Reel moves on."
            simulated_need = f"Hypothesis: this {age_band} aggregate segment may value a usable {theme} proof point; validate with later observed results."
        evidence = [f"Aggregate age band {age_band}: {share:g}% of the supplied audience snapshot."]
        if locations:
            location, location_share = locations[0]
            evidence.append(f"Top supplied location context: {location} ({location_share:g}%).")
        if terms:
            evidence.append(f"Recurring creator-history terms: {', '.join(f'#{term}' for term in terms[:2])}.")
        personas.append({
            "id": f"age-{age_band.lower().replace('+', 'plus').replace(' ', '-').replace('/', '-')}",
            "label": f"{theme} learner · {age_band}",
            "strategic_use": (
                f"Simulated planning lens for the aggregate {age_band} context. Use it to test whether a clearer hook or structure helps; "
                "it does not describe or predict any individual viewer."
            ),
            "observed_evidence": evidence,
            "inferred_interests": list(hypotheses["inferred_interests"])[:3],
            "suggested_hooks": list(hypotheses["suggested_hooks"])[:2],
            "simulated_need": simulated_need,
            "feedback_lens": feedback_lens,
            "limitations": [
                "Aggregate demographics do not show what any person watched, liked, or preferred.",
                "Content guidance is a hypothesis based on creator history and should be tested against later observed results.",
            ],
        })

    if personas:
        return personas

    if locations:
        location, share = locations[0]
        return [{
            "id": f"location-{location.lower().replace(' ', '-')}",
            "label": f"{location} planning lens",
            "strategic_use": "Simulated planning lens for available location context, not an individual viewer profile.",
            "observed_evidence": [f"Top supplied location context: {location} ({share:g}%)."],
            "inferred_interests": list(hypotheses["inferred_interests"])[:3],
            "suggested_hooks": list(hypotheses["suggested_hooks"])[:2],
            "simulated_need": "Hypothesis: available location context may help frame a future test, but it does not establish a viewer preference.",
            "feedback_lens": "Hypothesis to test: lead with one concrete outcome, then show the supporting proof before the Reel moves on.",
            "limitations": ["Location data does not prove a viewer preference or content-performance relationship."],
        }]
    return []
