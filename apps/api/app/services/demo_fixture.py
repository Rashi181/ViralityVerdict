"""Local-only ingestion for the supplied synthetic judge-demo fixture."""

from datetime import UTC, datetime
import json
from pathlib import Path

from pydantic import ValidationError

from app.schemas.imports import ImportedMedia


class DemoFixtureError(ValueError):
    pass


IGNORED_FIXTURE_FIELDS = {
    "synthetic_audience_personas",
    "recommendation_test_cases",
    "content_taxonomy",
    "interest_affinities_demo_estimates",
}


def _as_of(value: object) -> str:
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00")).isoformat()
        except ValueError:
            try:
                return datetime.fromisoformat(f"{value}T00:00:00+00:00").isoformat()
            except ValueError as error:
                raise DemoFixtureError("The fixture source.as_of value must be an ISO date or timestamp.") from error
    return datetime.now(UTC).isoformat()


def load_demo_fixture(path: str) -> tuple[list[dict], list[dict], list[str]]:
    """Validate and normalize raw fixture facts for the ordinary repositories.

    Pre-baked personas, labels, recommendation cases, taxonomy, and synthetic
    interest scores are intentionally never read by this function.
    """
    fixture_path = Path(path).expanduser().resolve()
    if not fixture_path.is_file() or fixture_path.stat().st_size > 2_000_000:
        raise DemoFixtureError("The configured local demonstration fixture is unavailable or too large.")
    try:
        payload = json.loads(fixture_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise DemoFixtureError("The configured demonstration fixture is not valid JSON.") from error

    source = payload.get("source")
    if not isinstance(source, dict) or source.get("type") != "synthetic_demo_fixture":
        raise DemoFixtureError("Demo mode accepts only a fixture explicitly labeled synthetic_demo_fixture.")
    posts = payload.get("posts")
    audience = payload.get("audience")
    if not isinstance(posts, list) or not posts or not isinstance(audience, dict):
        raise DemoFixtureError("The demonstration fixture needs non-empty posts and an audience object.")

    media: list[dict] = []
    for post in posts:
        if not isinstance(post, dict) or not isinstance(post.get("metrics"), dict):
            raise DemoFixtureError("Every demonstration post must contain a metrics object.")
        metrics = post["metrics"]
        try:
            normalized = ImportedMedia.model_validate({
                "media_id": post.get("id"),
                "published_at": post.get("published_at"),
                "caption": post.get("caption", ""),
                "media_type": "reel" if post.get("format") == "reel" else "post",
                "views": metrics.get("views", 0),
                "likes": metrics.get("likes", 0),
                "comments": metrics.get("comments", 0),
            }).model_dump(mode="json")
        except ValidationError as error:
            raise DemoFixtureError("One or more demonstration posts do not match Verdict's media schema.") from error
        # Preserve only raw, observed-like post fields. In particular, do not
        # retain any supplied label, persona, or recommendation on a post.
        normalized["hashtags"] = [tag for tag in post.get("hashtags", []) if isinstance(tag, str)]
        normalized["keywords"] = [keyword for keyword in post.get("keywords", []) if isinstance(keyword, str)]
        normalized["observed_metrics"] = {
            key: value for key, value in metrics.items() if isinstance(value, (int, float)) and value >= 0
        }
        media.append(normalized)

    as_of = _as_of(source.get("as_of"))
    label = "Synthetic demonstration data — local demo only, not Meta API data"
    aggregates: list[dict] = []
    field_map = {
        "age_distribution_pct": "age_distribution",
        "gender_distribution_pct": "gender_distribution",
        "top_countries_pct": "top_locations",
        "top_cities_pct": "top_locations",
        "total_followers": "follower_count",
        "languages_pct": "other",
        "follower_vs_nonfollower_reach_pct_last_30_days": "other",
        "gender_by_age_pct_of_total": "other",
        "activity_by_weekday_index_mon0": "other",
        "activity_by_hour_local_0_to_23": "other",
    }
    for key, field in field_map.items():
        value = audience.get(key)
        if isinstance(value, dict) and value:
            aggregates.append({"field": field, "values": value, "source": "synthetic_demo", "source_label": label, "as_of": as_of})
        elif isinstance(value, list) and value:
            aggregates.append({
                "field": field,
                "values": {str(index): item for index, item in enumerate(value) if isinstance(item, (int, float))},
                "source": "synthetic_demo",
                "source_label": label,
                "as_of": as_of,
            })
        elif isinstance(value, (int, float)):
            aggregates.append({"field": field, "values": {key: value}, "source": "synthetic_demo", "source_label": label, "as_of": as_of})

    if not aggregates:
        raise DemoFixtureError("The demonstration fixture contains no supported raw aggregate audience facts.")
    limitations = [
        "Synthetic demonstration data only. It is not a live Meta API response and must not be presented as OAuth-synced data.",
        f"The fixture's {', '.join(sorted(IGNORED_FIXTURE_FIELDS))} fields were intentionally ignored.",
        "Derived audience statements are hypotheses from the stored demographics and creator-history inputs, never individual viewer facts.",
    ]
    return media, aggregates, limitations
