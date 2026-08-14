from __future__ import annotations

from strands import Agent

from .library import list_titles
from .tools import fetch_story_tool


def create_agent() -> Agent:
    system_prompt = _build_system_prompt()
    return Agent(
        model="global.anthropic.claude-sonnet-4-6",
        system_prompt=system_prompt,
        tools=[fetch_story_tool],
        callback_handler=None,  # don't stream output to the console
    )


def _build_system_prompt() -> str:
    available_titles = list_titles()
    available_titles_list = "\n".join(available_titles)

    return f"""
You summarize stories from a small local collection.

Available stories:
{available_titles_list}

When the user asks for a summary of an available story, call fetch_story_tool
with the exact story title, then summarize the story in about 100 words.

If the user asks about a story that is not available, do not call the tool.
Say that the story is not in the collection and list the available stories.

Do not invent story contents.
"""
