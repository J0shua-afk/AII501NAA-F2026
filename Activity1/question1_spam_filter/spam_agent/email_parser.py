"""Turning the raw bytes of an .eml file into the facts the rules need.

An .eml file is plain text: header lines ("From: ...", "Subject: ..."), a blank
line, then the body. The body may be MIME *multipart* (a text body plus
attachments) and every part may be *transfer-encoded* (base64 or
quoted-printable) in some character set. Python's standard ``email`` package
parses all of that; this module decides which parts count as readable text.
"""

from __future__ import annotations

import email
from dataclasses import dataclass
from email.message import Message
from email.utils import getaddresses
from html.parser import HTMLParser
from typing import Optional

from .text_utils import normalize_domain


@dataclass(frozen=True)
class ParsedEmail:
    """The parts of an email the agent cares about."""

    sender_address: Optional[str]  # "alice@mail.example.com"; None if missing/malformed
    sender_domain: Optional[str]   # "mail.example.com";       None if missing/malformed
    body_text: str                 # readable body text, including text attachments


def parse_email(raw: bytes) -> ParsedEmail:
    """Parse one email. Malformed input never raises: missing pieces become None or ""."""
    message = email.message_from_bytes(raw)
    address = extract_sender_address(message)
    return ParsedEmail(
        sender_address=address,
        sender_domain=extract_domain(address),
        body_text=extract_body_text(message),
    )


# --- sender ---------------------------------------------------------------------

def extract_sender_address(message: Message) -> Optional[str]:
    """Return the single address in the From header, or None.

    Only the address is used, never the display name, so
    '"support@bank.example" <thief@evil.test>' is seen as coming from evil.test.
    If the header holds no address, or more than one (including the trick
    'support@bank.example <thief@evil.test>'), the sender is treated as unknown.
    """
    from_header = message.get("From")
    if from_header is None:
        return None
    addresses = [address for _name, address in getaddresses([str(from_header)]) if address]
    if len(addresses) != 1:
        return None
    return addresses[0].strip()


def extract_domain(address: Optional[str]) -> Optional[str]:
    """'alice@Mail.Example.com' -> 'mail.example.com'; None if the address is not usable."""
    if not address or "@" not in address:
        return None
    local_part, _, domain = address.rpartition("@")  # split at the LAST "@"
    if not local_part:  # "@example.com" has no mailbox name, so it is malformed
        return None
    return normalize_domain(domain)


# --- body -------------------------------------------------------------------------

def extract_body_text(message: Message) -> str:
    """Return all readable text of the email: the body plus any text attachments.

    * text/plain parts are used as they are; text/html parts have their tags removed;
    * parts of any other type (images, PDFs, archives, ...) cannot be read and are skipped;
    * multipart/alternative holds the SAME content in several formats (typically
      plain text + HTML), so only one version is read - otherwise every word
      would be counted twice.
    """
    chunks: list[str] = []
    _collect_text(message, chunks)
    return "\n".join(chunks)


def _collect_text(part: Message, chunks: list[str]) -> None:
    """Walk the MIME tree recursively, appending the text of readable parts to ``chunks``."""
    if part.is_multipart():
        subparts = part.get_payload()
        if part.get_content_subtype() == "alternative" and subparts:
            subparts = [_preferred_alternative(subparts)]
        for subpart in subparts:
            _collect_text(subpart, chunks)
        return

    maintype = part.get_content_maintype()
    if maintype == "text":
        text = _decode(part)
        if part.get_content_subtype() == "html":
            text = html_to_text(text)
        chunks.append(text)
    elif maintype == "multipart":
        # Broken MIME (e.g. "multipart/mixed" with no boundary): the parser could
        # not split it into parts, so read it as plain text rather than ignore it.
        chunks.append(_decode(part))
    # Any other type (image/*, application/*, audio/*, ...) is not readable text.


def _preferred_alternative(alternatives: list[Message]) -> Message:
    """Pick one version of a multipart/alternative: plain text, else HTML, else the last."""
    for wanted in ("text/plain", "text/html"):
        for alternative in alternatives:
            if alternative.get_content_type() == wanted:
                return alternative
    return alternatives[-1]  # RFC 2046: the last alternative is the richest one


def _decode(part: Message) -> str:
    """Undo the transfer encoding (base64 / quoted-printable) and the character set."""
    payload = part.get_payload(decode=True)  # bytes, with base64/QP already undone
    if payload is None:
        return ""
    charset = part.get_content_charset() or "utf-8"
    try:
        return payload.decode(charset, errors="replace")
    except (LookupError, ValueError):  # unknown or unusable charset name
        return payload.decode("utf-8", errors="replace")


class _HTMLTextExtractor(HTMLParser):
    """Collects the visible text of an HTML document (no tags, scripts or styles)."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)  # "&amp;" -> "&", "&#33;" -> "!"
        self.chunks: list[str] = []
        self._hidden_depth = 0  # > 0 while inside <script> or <style>

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self._hidden_depth += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._hidden_depth:
            self._hidden_depth -= 1

    def handle_data(self, data):
        if not self._hidden_depth:
            self.chunks.append(data)


def html_to_text(html: str) -> str:
    """Return the visible text of an HTML document."""
    extractor = _HTMLTextExtractor()
    extractor.feed(html)
    extractor.close()
    return " ".join(extractor.chunks)
