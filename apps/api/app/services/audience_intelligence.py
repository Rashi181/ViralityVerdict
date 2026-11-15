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
