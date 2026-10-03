"""Helpers shared by the Question 1 tests."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from spam_agent.lists import FilterLists

TESTS_DIR = Path(__file__).resolve().parent
FIXTURES = TESTS_DIR / "fixtures"
EMAIL_FIXTURES = FIXTURES / "emails"
LIST_FIXTURES = FIXTURES / "lists"
PROJECT_DIR = TESTS_DIR.parent
DEMO_DATA = PROJECT_DIR / "data"

# Small, fixed lists used by the agent tests (independent of the demo data files).
TEST_LISTS = FilterLists(
    allow_domains=frozenset({"trusted.example"}),
    restrict_domains=frozenset({"spam.test"}),
    bad_words=frozenset({"free", "cash", "prize", "winner", "lottery", "bonus", "click"}),
)


def make_email(sender: Optional[str], body: str, subject: str = "Test message") -> bytes:
    """Build the raw bytes of a minimal plain-text email (sender=None omits the From header)."""
    lines = [f"From: {sender}"] if sender is not None else []
    lines += ["To: me@example.com", f"Subject: {subject}", "", body]
    return "\r\n".join(lines).encode("utf-8")


def load_fixture(name: str) -> bytes:
    return (EMAIL_FIXTURES / name).read_bytes()
