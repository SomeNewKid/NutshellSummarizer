from __future__ import annotations

import json
from pathlib import Path
from typing import TypedDict

_STORIES_DIR = Path(__file__).resolve().parent / "stories"


class _StoryEntry(TypedDict):
    title: str
    filename: str


def list_titles() -> list[str]:
    manifest = _get_manifest()

    return [story["title"] for story in manifest]


def fetch_story(title: str) -> str | None:
    manifest = _get_manifest()
    normalized_title = _normalize_title(title)
    filename = None

    for story in manifest:
        story_title = _normalize_title(story["title"])
        if story_title == normalized_title:
            filename = story["filename"]
            break

    if not filename:
        return None

    with open(_STORIES_DIR / filename, encoding="utf-8") as file:
        return file.read()


def _get_manifest() -> list[_StoryEntry]:
    stories_manifest = _STORIES_DIR / "manifest.json"

    if not stories_manifest.exists():
        raise RuntimeError("Stories manifest does not exist.")

    if not stories_manifest.is_file():
        raise RuntimeError("Stories manifest is not a file.")

    with open(stories_manifest, encoding="utf-8") as file:
        manifest = json.load(file)

    if not isinstance(manifest, list):
        raise RuntimeError("Stories manifest must contain a list.")

    stories: list[_StoryEntry] = []

    for story in manifest:
        if not isinstance(story, dict):
            raise RuntimeError("Each story manifest entry must be an object.")

        title = story.get("title")
        filename = story.get("filename")

        if not isinstance(title, str):
            raise RuntimeError("Each story manifest entry must have a title.")

        if not isinstance(filename, str):
            raise RuntimeError("Each story manifest entry must have a filename.")

        stories.append({"title": title, "filename": filename})

    return stories


def _normalize_title(title: str) -> str:
    if not title:
        return ""
    title = " ".join(title.casefold().split())
    return title.lower().replace("-", "")
