"""Text helpers shared by the list loader, the email parser and the agent.

Two consistency guarantees live here:

* ``tokenize`` is used for BOTH the bad-word list and the email body, so the two
  can never disagree about what counts as a "word".
* ``normalize_domain`` is used for BOTH the list files and the sender's address,
  so "Example.COM." in a list and "user@example.com" in an email compare equal.
"""

from __future__ import annotations

import re
from typing import AbstractSet, Optional

# A word is a run of letters and/or digits (in any alphabet). Everything else -
# spaces, punctuation, symbols, apostrophes, hyphens, underscores - separates words.
#     "FREE!!! Cash, now"  ->  ["free", "cash", "now"]
#     "e-mail"             ->  ["e", "mail"]
_WORD = re.compile(r"[^\W_]+")

# A domain is one or more labels (letters, digits, "-" or "_") joined by single dots.
_DOMAIN = re.compile(r"[\w-]+(?:\.[\w-]+)*")


def tokenize(text: str) -> list[str]:
    """Split ``text`` into lower-case words, ignoring punctuation.

    ``casefold()`` is a stronger ``lower()`` designed for case-insensitive
    comparison (for example it also maps the German "ß" to "ss").
    """
    return _WORD.findall(text.casefold())


def normalize_domain(raw: str) -> Optional[str]:
    """Return the canonical form of a domain name, or ``None`` if it is not valid.

    "  Mail.Example.COM. "  ->  "mail.example.com"
    "not a domain"          ->  None
    """
    domain = raw.strip().casefold()
    if domain.endswith("."):  # one trailing dot is the DNS root ("example.com.")
        domain = domain[:-1]
    if domain and _DOMAIN.fullmatch(domain):
        return domain
    return None


def domain_matches(domain: Optional[str], listed: AbstractSet[str]) -> bool:
    """Return True if ``domain`` is on the list or is a sub-domain of a listed domain.

    The domain and each of its parent domains are looked up in the set:
        "mail.uni.example"  ->  "mail.uni.example", "uni.example", "example"
    so "mail.uni.example" matches a listed "uni.example", while the look-alike
    "fake-uni.example" does not (a match only happens at a "." boundary).
    """
    if not domain:
        return False
    labels = domain.split(".")
    return any(".".join(labels[i:]) in listed for i in range(len(labels)))
