from __future__ import annotations

from strands import tool

from .library import fetch_story, list_titles


@tool
def fetch_story_tool(title: str) -> str:
    """
    Fetch the full text of a story in the local collection.

    Use this tool only when the user asks about a specific story from the
    available collection. The title must be one of the known story titles.

    Arguments:
        title (str): the title of the story to return.

    Returns
        (str): the contents of the story if found,
               otherwise a list of available titles.
    """
    story = fetch_story(title)

    if story:
        return story

    titles = list_titles()
    return "Story not found.  Available titles are:, ".join(titles)
