"""Verdict's permanent read-only boundary for Instagram integrations.

No Meta write endpoint or write-capable permission belongs in this module.
"""

READ_ONLY_SCOPES = frozenset({"instagram_business_basic"})
DENIED_SCOPES = frozenset({
    "instagram_business_content_publishing",
    "instagram_business_manage_comments",
    "instagram_business_manage_messages",
    "instagram_content_publish",
    "instagram_manage_comments",
    "instagram_manage_messages",
    "pages_manage_posts",
})
ALLOWED_HTTP_METHODS = frozenset({"GET"})


def validate_scope_request(scopes: set[str]) -> tuple[str, ...]:
    if scopes & DENIED_SCOPES:
        raise ValueError("Verdict permanently denies Instagram publishing, comments, messages, and account-changing scopes.")
    if not scopes <= READ_ONLY_SCOPES:
        raise ValueError("Requested Instagram scope is not in Verdict's approved read-only allowlist.")
    return tuple(sorted(scopes))


def validate_api_method(method: str) -> str:
    normalized = method.upper()
    if normalized not in ALLOWED_HTTP_METHODS:
        raise ValueError("Verdict's Instagram adapter permits GET requests only.")
    return normalized
