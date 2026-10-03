"""Tests for text_utils.py (tokenizer, domains) and lists.py (loading the three lists)."""

import tempfile
import unittest
from pathlib import Path

from spam_agent.lists import (FilterLists, ListFileError, load_bad_words,
                              load_domain_list)
from spam_agent.text_utils import domain_matches, normalize_domain, tokenize
from tests.helpers import LIST_FIXTURES


class TestTokenize(unittest.TestCase):
    def test_lower_cases_every_word(self):
        self.assertEqual(tokenize("FREE Free free"), ["free", "free", "free"])

    def test_punctuation_separates_words(self):
        self.assertEqual(tokenize("FREE!!! Cash, prize... (winner?)"),
                         ["free", "cash", "prize", "winner"])

    def test_hyphens_apostrophes_and_underscores_split_words(self):
        self.assertEqual(tokenize("click-here don't free_money"),
                         ["click", "here", "don", "t", "free", "money"])

    def test_digits_and_accented_letters_are_word_characters(self):
        self.assertEqual(tokenize("Win $1000 GRATUIT énorme"),
                         ["win", "1000", "gratuit", "énorme"])

    def test_empty_and_symbol_only_text_has_no_words(self):
        self.assertEqual(tokenize(""), [])
        self.assertEqual(tokenize("$$$ !!! ---"), [])


class TestDomains(unittest.TestCase):
    def test_normalize_trims_lower_cases_and_drops_trailing_dot(self):
        self.assertEqual(normalize_domain("  Mail.Example.COM. "), "mail.example.com")

    def test_normalize_rejects_invalid_domains(self):
        for bad in ["", "   ", "not a domain", "bad..dots.example", ".leading.example", "a@b.example", "two-dots.example.."]:
            self.assertIsNone(normalize_domain(bad), bad)

    def test_exact_match(self):
        self.assertTrue(domain_matches("trusted.example", {"trusted.example"}))

    def test_sub_domain_matches_parent(self):
        self.assertTrue(domain_matches("mail.trusted.example", {"trusted.example"}))
        self.assertTrue(domain_matches("a.b.trusted.example", {"trusted.example"}))

    def test_look_alike_domains_do_not_match(self):
        listed = {"trusted.example"}
        self.assertFalse(domain_matches("nottrusted.example", listed))
        self.assertFalse(domain_matches("trusted.example.evil.test", listed))
        self.assertFalse(domain_matches("example", listed))  # a parent is not a sub-domain

    def test_unknown_sender_never_matches(self):
        self.assertFalse(domain_matches(None, {"trusted.example"}))
        self.assertFalse(domain_matches("", {"trusted.example"}))


class TestListLoading(unittest.TestCase):
    def test_domain_list_handles_comments_case_duplicates_and_prefixes(self):
        with self.assertLogs("spam_agent.lists", level="WARNING") as logs:
            domains = load_domain_list(LIST_FIXTURES / "allow_messy.txt")
        self.assertEqual(domains, {"example.com", "spaced.example", "at-prefix.example",
                                   "wildcard.example", "trailing-dot.example", "inline.example"})
        self.assertEqual(len(logs.output), 2)  # "not a domain" and "bad..dots.example"

    def test_bad_words_are_normalised_and_invalid_entries_skipped(self):
        with self.assertLogs("spam_agent.lists", level="WARNING") as logs:
            words = load_bad_words(LIST_FIXTURES / "bad_words_messy.txt")
        self.assertEqual(words, {"free", "cash", "prize", "winner"})
        self.assertEqual(len(logs.output), 2)  # "click here" (two words) and "$$$" (no word)

    def test_windows_byte_order_mark_is_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "allow.txt"
            path.write_bytes("\ufeffbom.example\n".encode("utf-8"))
            self.assertEqual(load_domain_list(path), {"bom.example"})

    def test_empty_file_gives_empty_list(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "empty.txt"
            path.write_text("# only a comment\n\n", encoding="utf-8")
            self.assertEqual(load_domain_list(path), frozenset())
            self.assertEqual(load_bad_words(path), frozenset())

    def test_missing_file_raises_list_file_error(self):
        with self.assertRaises(ListFileError):
            load_domain_list(LIST_FIXTURES / "does_not_exist.txt")

    def test_restrict_entry_covered_by_allow_list_is_reported(self):
        lists = FilterLists(allow_domains=frozenset({"example.com"}),
                            restrict_domains=frozenset({"promo.example.com", "spam.test"}),
                            bad_words=frozenset())
        self.assertEqual(lists.overlapping_domains(), ["promo.example.com"])

    def test_from_files_warns_about_conflicting_lists(self):
        with tempfile.TemporaryDirectory() as tmp:
            allow, restrict, words = (Path(tmp) / n for n in ("a.txt", "r.txt", "w.txt"))
            allow.write_text("both.example\n", encoding="utf-8")
            restrict.write_text("both.example\nspam.test\n", encoding="utf-8")
            words.write_text("free\n", encoding="utf-8")
            with self.assertLogs("spam_agent.lists", level="WARNING") as logs:
                lists = FilterLists.from_files(allow, restrict, words)
        self.assertIn("both.example", logs.output[0])
        self.assertEqual(lists.restrict_domains, {"both.example", "spam.test"})


if __name__ == "__main__":
    unittest.main()
