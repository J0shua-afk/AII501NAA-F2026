"""Tests for email_parser.py: sender extraction and readable-body extraction."""

import unittest

from spam_agent.email_parser import html_to_text, parse_email
from spam_agent.text_utils import tokenize
from tests.helpers import load_fixture, make_email


class TestSenderExtraction(unittest.TestCase):
    def domain_of(self, from_header):
        return parse_email(make_email(from_header, "hello")).sender_domain

    def test_plain_address(self):
        self.assertEqual(self.domain_of("alice@example.com"), "example.com")

    def test_display_name_and_upper_case(self):
        parsed = parse_email(make_email("Alice Smith <Alice@Mail.EXAMPLE.com>", "hi"))
        self.assertEqual(parsed.sender_address, "Alice@Mail.EXAMPLE.com")
        self.assertEqual(parsed.sender_domain, "mail.example.com")

    def test_display_name_is_never_used_as_the_sender(self):
        # The display name pretends to be the bank; the real address is evil.test.
        self.assertEqual(self.domain_of('"support@bank.example" <thief@evil.test>'), "evil.test")

    def test_ambiguous_header_is_treated_as_unknown(self):
        # Unquoted trick: never let it be read as bank.example.
        self.assertIsNone(self.domain_of("support@bank.example <thief@evil.test>"))

    def test_missing_from_header(self):
        parsed = parse_email(make_email(None, "hello"))
        self.assertIsNone(parsed.sender_address)
        self.assertIsNone(parsed.sender_domain)

    def test_malformed_from_headers_give_unknown_domain(self):
        for header in ["not an email address", "<>", "user@", "@example.com.."]:
            self.assertIsNone(self.domain_of(header), header)

    def test_trailing_dot_and_whitespace_are_normalised(self):
        self.assertEqual(self.domain_of("  bob@Example.org.  "), "example.org")


class TestBodyExtraction(unittest.TestCase):
    def test_simple_plain_text_body(self):
        parsed = parse_email(make_email("a@example.com", "Just a FREE sample."))
        self.assertIn("Just a FREE sample.", parsed.body_text)

    def test_subject_is_not_part_of_the_body(self):
        parsed = parse_email(make_email("a@example.com", "hello", subject="FREE CASH PRIZE"))
        self.assertNotIn("CASH", parsed.body_text)

    def test_text_attachments_are_read_but_binary_attachments_are_not(self):
        body = parse_email(load_fixture("multipart_with_attachments.eml")).body_text
        self.assertIn("BODYMARKER", body)
        self.assertIn("ATTACHMARKER", body)  # text/plain attachment
        self.assertNotIn("PDFMARKER", body)  # application/pdf is not readable text

    def test_alternative_versions_are_read_only_once(self):
        body = parse_email(load_fixture("alternative_plain_and_html.eml")).body_text
        self.assertIn("PLAINMARKER", body)
        self.assertNotIn("HTMLMARKER", body)
        self.assertEqual(tokenize(body).count("free"), 1)  # not double counted

    def test_html_tags_scripts_and_styles_are_removed(self):
        body = parse_email(load_fixture("html_only.eml")).body_text
        self.assertIn("VISIBLEMARKER", body)
        self.assertIn("&", body)  # &amp; decoded
        for hidden in ("SCRIPTMARKER", "STYLEMARKER", "<b>", "<p>"):
            self.assertNotIn(hidden, body)

    def test_base64_body_is_decoded(self):
        body = parse_email(load_fixture("base64_utf8.eml")).body_text
        self.assertIn("Café gratuit: FREE money", body)

    def test_quoted_printable_body_is_decoded(self):
        body = parse_email(load_fixture("quoted_printable.eml")).body_text
        self.assertIn("This word is free and costs $3 only!", body)

    def test_broken_multipart_is_still_read(self):
        body = parse_email(load_fixture("multipart_without_boundary.eml")).body_text
        self.assertIn("NOBOUNDARYMARKER", body)

    def test_unknown_charset_falls_back_to_utf8(self):
        body = parse_email(load_fixture("unknown_charset.eml")).body_text
        self.assertIn("CHARSETMARKER", body)

    def test_forwarded_message_body_is_read(self):
        body = parse_email(load_fixture("forwarded_message.eml")).body_text
        self.assertIn("INNERMARKER", body)

    def test_empty_and_header_only_input(self):
        empty = parse_email(b"")
        self.assertIsNone(empty.sender_domain)
        self.assertEqual(empty.body_text.strip(), "")
        headers_only = parse_email(b"From: a@example.com\r\nSubject: hi\r\n")
        self.assertEqual(headers_only.sender_domain, "example.com")
        self.assertEqual(headers_only.body_text.strip(), "")

    def test_html_to_text_keeps_words_apart(self):
        self.assertEqual(tokenize(html_to_text("<p>free</p><p>cash</p>")), ["free", "cash"])


if __name__ == "__main__":
    unittest.main()
