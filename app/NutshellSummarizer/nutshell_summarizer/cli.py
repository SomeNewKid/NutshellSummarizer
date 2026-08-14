"""Command-line interface for the application."""

from __future__ import annotations

import sys

from .agent import create_agent


def main(argv: list[str] | None = None) -> int:
    """Run the command-line interface."""
    prompt = _get_prompt(argv)
    if not prompt:
        example = "Summarize the story of Iron Hans"
        raise SystemExit(f'Usage: python -m nutshell_summarizer "{example}"')

    agent = create_agent()
    response = agent(prompt)
    print(response)
    return 0


def _get_prompt(argv: list[str] | None = None) -> str:
    args = sys.argv[1:] if argv is None else argv
    if not args:
        return ""

    return args[0]
