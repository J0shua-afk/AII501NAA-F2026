"""Loading the agent's knowledge: the allow list, restrict list and bad-word list.

All three files use the same simple format:

* one entry per line;
* blank lines are ignored, and anything after a ``#`` is a comment;
* case and surrounding whitespace do not matter, and duplicates are merged.

Domain entries may be written as ``example.com``, ``@example.com`` or
``*.example.com``; all three mean "example.com and its sub-domains".
Bad-word entries must be a single word (as defined by ``text_utils.tokenize``).
Invalid entries are skipped with a warning instead of stopping the program.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from .text_utils import domain_matches, normalize_domain, tokenize

logger = logging.getLogger(__name__)


class ListFileError(Exception):
    """A list file is missing or cannot be read."""


def read_entries(path: Path) -> list[tuple[int, str]]:
    """Return ``(line_number, entry)`` for every non-blank, non-comment line."""
    try:
        # "utf-8-sig" also strips the invisible byte-order mark that some
        # Windows editors (e.g. Notepad) put at the start of a file.
        text = Path(path).read_text(encoding="utf-8-sig")
    except (OSError, UnicodeDecodeError) as exc:
        raise ListFileError(f"cannot read list file '{path}': {exc}") from exc

    entries = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        entry = line.split("#", 1)[0].strip()
        if entry:
            entries.append((line_number, entry))
    return entries


def load_domain_list(path: Path) -> frozenset[str]:
    """Load an allow/restrict list as a set of normalised domain names."""
    domains = set()
    for line_number, entry in read_entries(path):
        domain = normalize_domain(entry.removeprefix("@").removeprefix("*."))
        if domain is None:
            logger.warning("%s, line %d: '%s' is not a valid domain - ignored",
                           path, line_number, entry)
        else:
            domains.add(domain)
    return frozenset(domains)


def load_bad_words(path: Path) -> frozenset[str]:
    """Load the bad-word list as a set of normalised single words."""
    words = set()
    for line_number, entry in read_entries(path):
        tokens = tokenize(entry)
        if len(tokens) == 1:
            words.add(tokens[0])
        else:
            logger.warning("%s, line %d: '%s' is not a single word - ignored",
                           path, line_number, entry)
    return frozenset(words)


@dataclass(frozen=True)
class FilterLists:
    """The three lists the agent consults, already normalised."""

    allow_domains: frozenset[str]
    restrict_domains: frozenset[str]
    bad_words: frozenset[str]

    @classmethod
    def from_files(cls, allow_path: Path, restrict_path: Path,
                   bad_words_path: Path) -> "FilterLists":
        """Load all three lists and warn about contradictory entries."""
        lists = cls(
            allow_domains=load_domain_list(allow_path),
            restrict_domains=load_domain_list(restrict_path),
            bad_words=load_bad_words(bad_words_path),
        )
        for domain in lists.overlapping_domains():
            logger.warning(
                "'%s' is on the restrict list but is also covered by the allow list; "
                "the allow-list rule is checked first, so its mail will NOT be spam",
                domain)
        return lists

    def overlapping_domains(self) -> list[str]:
        """Restrict-list entries that the allow list overrides (a configuration conflict)."""
        return sorted(d for d in self.restrict_domains
                      if domain_matches(d, self.allow_domains))
