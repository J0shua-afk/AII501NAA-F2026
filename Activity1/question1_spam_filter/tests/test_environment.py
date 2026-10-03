"""Tests for environment.py (sensor/actuator), an end-to-end run and main.py."""

import contextlib
import io
import shutil
import tempfile
import unittest
from pathlib import Path

import main
from spam_agent.agent import Action, SpamFilterAgent
from spam_agent.environment import MailEnvironment
from spam_agent.lists import FilterLists
from tests.helpers import DEMO_DATA, TEST_LISTS, make_email

# Where every demo email must end up, and which rule must put it there.
EXPECTED_DEMO_RESULTS = {
    "01_normal_email.eml": ("email", "DEFAULT"),
    "02_allow_list_newsletter.eml": ("email", "ALLOW_LIST"),
    "03_allow_list_subdomain.eml": ("email", "ALLOW_LIST"),
    "04_restrict_list_no_bad_words.eml": ("spam", "RESTRICT_LIST"),
    "05_lottery_scam.eml": ("spam", "BAD_WORDS"),
    "06_exactly_five_bad_words.eml": ("email", "DEFAULT"),
    "07_six_bad_words_mixed_case.eml": ("spam", "BAD_WORDS"),
    "08_same_word_repeated.eml": ("spam", "BAD_WORDS"),
    "09_text_attachment.eml": ("spam", "BAD_WORDS"),
    "10_html_and_plain_versions.eml": ("email", "DEFAULT"),
    "11_base64_encoded_body.eml": ("spam", "BAD_WORDS"),
    "12_lookalike_domain.eml": ("spam", "BAD_WORDS"),
    "13_missing_from_header.eml": ("email", "DEFAULT"),
    "14_malformed_from_header.eml": ("spam", "BAD_WORDS"),
}


class EnvironmentTestCase(unittest.TestCase):
    """Creates a temporary inbox and output folder for every test."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.inbox = self.root / "inbox"
        self.output = self.root / "output"
        self.inbox.mkdir()

    def tearDown(self):
        self._tmp.cleanup()

    def add_email(self, name, sender, body):
        (self.inbox / name).write_bytes(make_email(sender, body))

    def names_in(self, folder):
        path = self.output / folder
        return sorted(p.name for p in path.iterdir()) if path.exists() else []


class TestFilePlacement(EnvironmentTestCase):
    def setUp(self):
        super().setUp()
        self.add_email("a_spam.eml", "x@spam.test", "hello")
        self.add_email("b_ham.eml", "x@trusted.example", "free cash prize winner lottery bonus")
        self.add_email("c_ham.eml", "x@unknown.example", "see you soon")

    def test_copy_mode_files_each_email_and_keeps_the_inbox(self):
        results = MailEnvironment(self.inbox, self.output).run(SpamFilterAgent(TEST_LISTS))
        self.assertEqual(self.names_in("spam"), ["a_spam.eml"])
        self.assertEqual(self.names_in("email"), ["b_ham.eml", "c_ham.eml"])
        self.assertEqual(len(list(self.inbox.iterdir())), 3)  # originals untouched
        self.assertEqual([r.filename for r in results], ["a_spam.eml", "b_ham.eml", "c_ham.eml"])

    def test_move_mode_empties_the_inbox(self):
        MailEnvironment(self.inbox, self.output, move=True).run(SpamFilterAgent(TEST_LISTS))
        self.assertEqual(list(self.inbox.iterdir()), [])
        self.assertEqual(self.names_in("spam"), ["a_spam.eml"])
        self.assertEqual(self.names_in("email"), ["b_ham.eml", "c_ham.eml"])

    def test_move_mode_never_overwrites_an_existing_file(self):
        (self.output / "spam").mkdir(parents=True)
        (self.output / "spam" / "a_spam.eml").write_text("older email")
        MailEnvironment(self.inbox, self.output, move=True).run(SpamFilterAgent(TEST_LISTS))
        self.assertEqual(self.names_in("spam"), ["a_spam.eml", "a_spam_1.eml"])
        self.assertEqual((self.output / "spam" / "a_spam.eml").read_text(), "older email")

    def test_rerun_after_list_change_keeps_each_email_in_one_folder(self):
        MailEnvironment(self.inbox, self.output).run(SpamFilterAgent(TEST_LISTS))
        no_restrict = FilterLists(TEST_LISTS.allow_domains, frozenset(), TEST_LISTS.bad_words)
        MailEnvironment(self.inbox, self.output).run(SpamFilterAgent(no_restrict))
        self.assertEqual(self.names_in("spam"), [])
        self.assertEqual(self.names_in("email"), ["a_spam.eml", "b_ham.eml", "c_ham.eml"])


class TestRobustness(EnvironmentTestCase):
    def test_non_eml_files_and_folders_are_ignored(self):
        self.add_email("real.EML", "x@unknown.example", "hi")
        (self.inbox / "notes.txt").write_text("free free free free free free")
        (self.inbox / "folder.eml").mkdir()
        results = MailEnvironment(self.inbox, self.output).run(SpamFilterAgent(TEST_LISTS))
        self.assertEqual([r.filename for r in results], ["real.EML"])

    def test_email_that_fails_is_reported_and_left_in_the_inbox(self):
        self.add_email("bad.eml", "x@unknown.example", "hi")
        self.add_email("good.eml", "x@unknown.example", "hi")

        class FailsOnFirstEmail(SpamFilterAgent):
            calls = 0

            def program(self, percept):
                FailsOnFirstEmail.calls += 1
                if FailsOnFirstEmail.calls == 1:
                    raise ValueError("simulated failure")
                return super().program(percept)

        env = MailEnvironment(self.inbox, self.output, move=True)
        with self.assertLogs("spam_agent.environment", level="ERROR"):
            results = env.run(FailsOnFirstEmail(TEST_LISTS))
        self.assertIn("simulated failure", results[0].error)
        self.assertIsNone(results[1].error)
        self.assertEqual([p.name for p in self.inbox.iterdir()], ["bad.eml"])
        self.assertEqual(self.names_in("email"), ["good.eml"])

    def test_missing_inbox_raises_file_not_found(self):
        env = MailEnvironment(self.root / "nope", self.output)
        with self.assertRaises(FileNotFoundError):
            env.run(SpamFilterAgent(TEST_LISTS))

    def test_empty_inbox_produces_no_results(self):
        self.assertEqual(MailEnvironment(self.inbox, self.output).run(SpamFilterAgent(TEST_LISTS)), [])


class TestEndToEndOnDemoData(EnvironmentTestCase):
    """Runs the real agent on a copy of data/ and checks every demo email."""

    def test_every_demo_email_is_filed_as_documented(self):
        shutil.copytree(DEMO_DATA / "inbox", self.inbox, dirs_exist_ok=True)
        lists = FilterLists.from_files(DEMO_DATA / "allow_list.txt",
                                       DEMO_DATA / "restrict_list.txt",
                                       DEMO_DATA / "bad_words.txt")
        results = MailEnvironment(self.inbox, self.output).run(SpamFilterAgent(lists))

        actual = {r.filename: (r.decision.action.value, r.decision.rule.name) for r in results}
        self.assertEqual(actual, EXPECTED_DEMO_RESULTS)
        for name, (folder, _rule) in EXPECTED_DEMO_RESULTS.items():
            other = "email" if folder == "spam" else "spam"
            self.assertTrue((self.output / folder / name).exists(), name)
            self.assertFalse((self.output / other / name).exists(), name)


class TestCommandLine(EnvironmentTestCase):
    def run_main(self, *args):
        with contextlib.redirect_stdout(io.StringIO()) as out, \
             contextlib.redirect_stderr(io.StringIO()) as err:
            code = main.main([str(a) for a in args])
        return code, out.getvalue(), err.getvalue()

    def list_args(self):
        return ["--allow-list", DEMO_DATA / "allow_list.txt",
                "--restrict-list", DEMO_DATA / "restrict_list.txt",
                "--bad-words", DEMO_DATA / "bad_words.txt"]

    def test_successful_run_returns_0_and_prints_a_summary(self):
        shutil.copytree(DEMO_DATA / "inbox", self.inbox, dirs_exist_ok=True)
        code, out, _ = self.run_main("--inbox", self.inbox, "--output", self.output, *self.list_args())
        self.assertEqual(code, 0)
        self.assertIn("Result: 8 spam, 6 email, 0 error(s)", out)

    def test_missing_list_file_returns_2(self):
        code, _, err = self.run_main("--inbox", self.inbox, "--output", self.output,
                                     "--bad-words", self.root / "missing.txt")
        self.assertEqual(code, 2)
        self.assertIn("cannot read list file", err)

    def test_missing_inbox_returns_2(self):
        code, _, err = self.run_main("--inbox", self.root / "nope", "--output", self.output,
                                     *self.list_args())
        self.assertEqual(code, 2)
        self.assertIn("inbox directory not found", err)


if __name__ == "__main__":
    unittest.main()
