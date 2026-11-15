"""Read-only provider adapters for a creator-owned private Reel draft."""
from __future__ import annotations

import json
import logging
import time
import base64
from pathlib import Path
from typing import Protocol

from pydantic import BaseModel, Field, ValidationError

from app.schemas.videos import ReelFinding

logger = logging.getLogger(__name__)


class GeminiReelAnalysis(BaseModel):
    findings: list[ReelFinding] = Field(default_factory=list, max_length=8)
    summary: str = Field(min_length=1, max_length=600)
    limitations: list[str] = Field(default_factory=list, max_length=5)


class ReelAnalyzer(Protocol):
    def analyze(self, private_video_path: Path, *, content_type: str, duration_seconds: float, frame_paths: list[Path]) -> GeminiReelAnalysis: ...


class GeminiUnavailableError(RuntimeError):
    pass


def _safe_groq_error(error: Exception) -> str:
    """Turn provider failures into a useful, non-sensitive recovery message."""
    status_code = getattr(error, "status_code", None)
    if status_code == 401:
        return "Groq rejected the local API key. Check GROQ_API_KEY in .env, then restart the API."
    if status_code in {402, 429}:
        return "Groq has no available quota right now or is rate-limiting this key. Check the Groq console, wait briefly, then try again."
    if status_code == 400:
        return "Groq rejected this vision request. Confirm GROQ_REEL_MODEL=qwen/qwen3.8-27b, then upload a fresh, short Reel and try again."
    if status_code in {404, 422}:
        return "Groq could not use the configured vision model. Set GROQ_REEL_MODEL=qwen/qwen3.8-27b and restart the API."
    if status_code is not None and status_code >= 500:
        return "Groq is temporarily unavailable. Your draft was not changed; try again shortly."
    return "Groq could not analyze these private strategic frames right now. Your draft was not changed; check the API terminal for the provider status, then try again."


def _safe_xai_error(status_code: int | None) -> str:
    if status_code == 401:
        return "xAI rejected the local Grok key. Check XAI_API_KEY in .env, then restart the API."
    if status_code in {402, 429}:
        return "xAI has no available quota right now or is rate-limiting this key. Check the xAI console, wait briefly, then try again."
    if status_code in {400, 404, 422}:
        return "xAI rejected this vision request. Confirm XAI_REEL_MODEL=grok-4.7, then upload a fresh short Reel and try again."
    if status_code is not None and status_code >= 500:
        return "xAI is temporarily unavailable. Your draft was not changed; try again shortly."
    return "xAI could not analyze these private strategic frames right now. Your draft was not changed; check the API terminal for the provider status, then try again."


def _normalize_xai_analysis(raw: object, duration_seconds: float) -> dict:
    """Normalize a valid xAI JSON response to Verdict's small persisted schema.

    Grok can use descriptive focus names such as “Hook promise”. We retain the
    accompanying observation/recommendation but map the category into the
    fixed, user-facing evidence taxonomy rather than discarding a useful reply.
    """
    if not isinstance(raw, dict):
        raise ValueError("xAI response must be a JSON object")
    focus_labels = {
        "hook": "hook", "opening": "hook", "pace": "pacing", "rhythm": "pacing",
        "scene": "visual_change", "transition": "visual_change", "visual": "visual_change", "proof": "visual_change",
        "audio": "audio", "sound": "audio", "voice": "audio",
        "caption": "on_screen_text", "text": "on_screen_text", "readability": "on_screen_text",
        "cta": "cta", "call to action": "cta", "accessib": "accessibility",
    }
    findings: list[dict] = []
    for item in raw.get("findings", [])[:5]:
        if not isinstance(item, dict):
            continue
        descriptive_focus = str(item.get("focus", "clarity"))
        lowered = descriptive_focus.lower()
        focus = next((category for phrase, category in focus_labels.items() if phrase in lowered), "clarity")
        severity = str(item.get("severity", "medium")).lower()
        findings.append({
            "timestamp_seconds": item.get("timestamp_seconds", 0),
            "focus": focus,
            "severity": severity if severity in {"low", "medium", "high"} else "medium",
            "observation": str(item.get("observation", "")),
            "recommendation": str(item.get("recommendation", "")),
        })
    limitations = raw.get("limitations", [])
    if isinstance(limitations, str):
        limitations = [limitations]
    if not isinstance(limitations, list):
        limitations = []
    return {
        "findings": findings,
        "summary": str(raw.get("summary", "xAI Grok returned strategic still-frame feedback.")),
        "limitations": [str(item) for item in limitations[:5]],
    }


class GeminiReelAnalyzer:
    """Uploads one private draft, requests JSON only, then deletes the remote file."""

    def __init__(self, api_key: str | None, model: str) -> None:
        self.api_key = api_key
        self.model = model

    def analyze(self, private_video_path: Path, *, content_type: str, duration_seconds: float, frame_paths: list[Path]) -> GeminiReelAnalysis:
        if not self.api_key:
            raise GeminiUnavailableError("Gemini is not configured locally. Add GEMINI_API_KEY to the local .env file, then restart the API.")
        try:
            from google import genai
            from google.genai import types
        except ImportError as error:  # pragma: no cover - guarded by project dependency
            raise GeminiUnavailableError("The Gemini SDK is not installed in the API environment.") from error

        client = genai.Client(api_key=self.api_key)
        uploaded = None
        try:
            uploaded = client.files.upload(file=str(private_video_path), config=types.UploadFileConfig(mime_type=content_type))
            deadline = time.monotonic() + 60
            while getattr(getattr(uploaded, "state", None), "name", None) != "ACTIVE":
                if time.monotonic() >= deadline:
                    raise GeminiUnavailableError("Gemini did not finish preparing this private video within 60 seconds. Try a shorter Reel.")
                time.sleep(2)
                uploaded = client.files.get(name=uploaded.name)
            prompt = f"""Analyze this creator-owned private Reel draft ({duration_seconds:.1f} seconds) for pre-publication editing.
Return only the requested JSON. Do not describe it frame by frame. Instead, inspect strategically:
- concentrate on the first five seconds for the hook;
- sample the rest sparsely for narrative, pacing, clarity, audio, on-screen text, CTA, and accessibility;
- add a finding whenever there is a material visual/scene change that affects comprehension or engagement.
Every finding must be timestamped within 0 to {duration_seconds:.1f}. Observations must be visible/audible in the video; recommendations are hypotheses, not predicted viewer behavior. Do not invent demographics, retention curves, audience reactions, or performance statistics."""
            result = client.models.generate_content(
                model=self.model,
                contents=[uploaded, prompt],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_json_schema=GeminiReelAnalysis.model_json_schema(),
                    temperature=0.2,
                    max_output_tokens=1800,
                ),
            )
            try:
                analysis = GeminiReelAnalysis.model_validate(json.loads(result.text or "{}"))
            except (json.JSONDecodeError, ValidationError) as error:
                raise GeminiUnavailableError("Gemini returned an invalid analysis. No feedback was saved; try again.") from error
            valid_findings = [finding for finding in analysis.findings if 0 <= finding.timestamp_seconds <= duration_seconds]
            return analysis.model_copy(update={"findings": valid_findings})
        except GeminiUnavailableError:
            raise
        except Exception as error:  # Provider failures are intentionally not exposed to the browser.
            logger.exception("Gemini Reel analysis failed with %s", type(error).__name__)
            raise GeminiUnavailableError("Gemini could not analyze this private Reel right now. Your draft was not changed; try again shortly.") from error
        finally:
            if uploaded is not None:
                try:
                    client.files.delete(name=uploaded.name)
                except Exception:
                    pass


class GroqReelAnalyzer:
    """Low-latency fallback: one vision request over three selected private frames."""

    def __init__(self, api_key: str | None, model: str) -> None:
        self.api_key = api_key
        self.model = model

    def analyze(self, private_video_path: Path, *, content_type: str, duration_seconds: float, frame_paths: list[Path]) -> GeminiReelAnalysis:
        if not self.api_key:
            raise GeminiUnavailableError("Groq is not configured locally. Add GROQ_API_KEY to the local .env file, then restart the API.")
        selected = [path for path in frame_paths if path.is_file()][:3]
        if not selected:
            raise GeminiUnavailableError("No private strategic frames are available. Upload the draft again before Groq analysis.")
        try:
            from groq import Groq
            images = [
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"}}
                for path in selected
            ]
            prompt = f"""You are reviewing three strategic stills from a creator-owned private Reel draft lasting {duration_seconds:.1f} seconds.
The frames represent the opening, the end of the opening hook, and a material visual change or later body moment. Return JSON only with findings and summary.
Do not claim to have watched every frame or heard audio. Do not invent demographics, retention, viewer reactions, performance metrics, or timestamps outside 0 to {duration_seconds:.1f}. Give at most five practical observations and edits."""
            completion = Groq(api_key=self.api_key).chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": [{"type": "text", "text": prompt}, *images]}],
                response_format={"type": "json_object"},
                temperature=0.2,
                max_completion_tokens=1200,
            )
            payload = completion.choices[0].message.content or "{}"
            analysis = GeminiReelAnalysis.model_validate(json.loads(payload))
            return analysis.model_copy(update={"findings": [finding for finding in analysis.findings if 0 <= finding.timestamp_seconds <= duration_seconds]})
        except GeminiUnavailableError:
            raise
        except (json.JSONDecodeError, ValidationError) as error:
            logger.exception("Groq Reel response did not match Verdict's schema")
            raise GeminiUnavailableError("Groq returned an invalid analysis. No feedback was saved; try again.") from error
        except Exception as error:
            logger.exception("Groq Reel analysis failed with %s", type(error).__name__)
            raise GeminiUnavailableError(_safe_groq_error(error)) from error


class XAIReelAnalyzer:
    """xAI Grok vision adapter for the same bounded strategic-frame workflow."""

    def __init__(self, api_key: str | None, model: str) -> None:
        self.api_key = api_key
        self.model = model

    def analyze(self, private_video_path: Path, *, content_type: str, duration_seconds: float, frame_paths: list[Path]) -> GeminiReelAnalysis:
        del private_video_path, content_type
        if not self.api_key:
            raise GeminiUnavailableError("xAI Grok is not configured locally. Add XAI_API_KEY to the local .env file, then restart the API.")
        selected = [path for path in frame_paths if path.is_file()][:3]
        if not selected:
            raise GeminiUnavailableError("No private strategic frames are available. Upload the draft again before Grok analysis.")
        images = [
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"}}
            for path in selected
        ]
        prompt = f"""You are reviewing three strategic stills from a creator-owned private Reel draft lasting {duration_seconds:.1f} seconds.
The stills represent the opening, the end of the opening hook, and a material visual change or later body moment. Return one JSON object with findings, summary, and limitations. Each finding needs timestamp_seconds, focus, severity, observation, and recommendation. For focus, use only: hook, pacing, visual_change, clarity, audio, on_screen_text, cta, or accessibility. For severity, use only: low, medium, or high. Limitations must be an array of strings.
Do not claim to have watched every frame or heard audio. Do not invent demographics, retention, viewer reactions, performance metrics, or timestamps outside 0 to {duration_seconds:.1f}. Give at most five practical observations and edits."""
        try:
            import httpx

            response = httpx.post(
                "https://api.x.ai/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                json={"model": self.model, "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}, *images]}], "temperature": 0.2},
                timeout=75,
            )
            if response.status_code >= 400:
                raise GeminiUnavailableError(_safe_xai_error(response.status_code))
            payload = response.json()["choices"][0]["message"]["content"]
            if payload.startswith("```"):
                payload = payload.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            analysis = GeminiReelAnalysis.model_validate(_normalize_xai_analysis(json.loads(payload), duration_seconds))
            return analysis.model_copy(update={"findings": [finding for finding in analysis.findings if 0 <= finding.timestamp_seconds <= duration_seconds]})
        except GeminiUnavailableError:
            raise
        except (json.JSONDecodeError, KeyError, TypeError, ValidationError, ValueError) as error:
            logger.exception("xAI Grok Reel response did not match Verdict's schema")
            raise GeminiUnavailableError("xAI Grok returned an invalid analysis. No feedback was saved; try again.") from error
        except Exception as error:
            logger.exception("xAI Grok Reel analysis failed with %s", type(error).__name__)
            raise GeminiUnavailableError(_safe_xai_error(getattr(error, "status_code", None))) from error
