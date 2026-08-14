"""Smoke tests for Nutshell Summarizer."""

from nutshell_summarizer.cli import main


def test_test_suite_is_configured() -> None:
    """Verify the CLI module can be imported and invoked."""
    assert main(["Once upon a time..."]) == 0
