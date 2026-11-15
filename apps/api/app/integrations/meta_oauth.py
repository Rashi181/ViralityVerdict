"""Small, auditable Meta OAuth/read client.

OAuth token exchange is authentication, not an Instagram content operation. Every
subsequent Graph request is validated by the GET-only Instagram policy.
"""

from dataclasses import dataclass
from typing import Protocol
from urllib.parse import urlencode
from urllib.request import urlopen
import json

from app.integrations.instagram_policy import READ_ONLY_SCOPES, validate_api_method


@dataclass(frozen=True)
class MetaSnapshot:
    account_id: str
    username: str | None
    media: list[dict]
    audience: list[dict]


class MetaClient(Protocol):
    def authorization_url(self, state: str) -> str: ...
    def exchange_code(self, code: str) -> str: ...
    def read_snapshot(self, access_token: str) -> MetaSnapshot: ...
    def revoke(self, access_token: str) -> bool: ...


class FacebookLoginMetaClient:
    def __init__(self, app_id: str, app_secret: str, redirect_uri: str, api_version: str) -> None:
        self.app_id, self.app_secret, self.redirect_uri, self.api_version = app_id, app_secret, redirect_uri, api_version

    def authorization_url(self, state: str) -> str:
        query = urlencode({"client_id": self.app_id, "redirect_uri": self.redirect_uri, "state": state, "response_type": "code", "scope": ",".join(sorted(READ_ONLY_SCOPES))})
        return f"https://www.facebook.com/{self.api_version}/dialog/oauth?{query}"

    def _get(self, path: str, params: dict[str, str]) -> dict:
        validate_api_method("GET")
        query = urlencode(params)
        with urlopen(f"https://graph.facebook.com/{self.api_version}/{path}?{query}", timeout=10) as response:  # noqa: S310 - fixed Meta host
            return json.loads(response.read().decode())

    def exchange_code(self, code: str) -> str:
        # Meta supports this OAuth exchange as a GET request; it is deliberately not a content write.
        payload = self._get("oauth/access_token", {"client_id": self.app_id, "client_secret": self.app_secret, "redirect_uri": self.redirect_uri, "code": code})
        token = payload.get("access_token")
        if not isinstance(token, str) or not token:
            raise ValueError("Meta did not return an access token")
        return token

    def read_snapshot(self, access_token: str) -> MetaSnapshot:
        pages = self._get("me/accounts", {"access_token": access_token, "fields": "id,name,instagram_business_account{id,username,media.limit(100){id,caption,timestamp,media_type,media_product_type,like_count,comments_count,views}}"})
        for page in pages.get("data", []):
            account = page.get("instagram_business_account") or {}
            if account.get("id"):
                return MetaSnapshot(account_id=str(account["id"]), username=account.get("username"), media=list((account.get("media") or {}).get("data") or []), audience=[])
        raise ValueError("No Professional Instagram account linked to an authorized Facebook Page was returned by Meta")

    def revoke(self, access_token: str) -> bool:
        # Remote revoke is intentionally deferred: it needs a documented Meta endpoint and a separate security review.
        return False
