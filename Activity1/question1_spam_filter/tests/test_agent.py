"""Tests for agent.py: INTERPRET-INPUT, the rule table and RULE-MATCH."""

import unittest

from spam_agent.agent import (BAD_WORD_THRESHOLD, RULES, Action, EmailState,
                              SpamFilterAgent)
from spam_agent.lists import FilterLists
from tests.helpers import TEST_LISTS, make_email

SIX_BAD_WORDS = "free cash prize winner lottery bonus"
FIVE_BAD_WORDS = "free cash prize winner lottery"


class TestRules(unittest.TestCase):
    def setUp(self):
        self.agent = SpamFilterAgent(TEST_LISTS)

    def decide(self, sender, body, subject="Test message"):
        return self.agent.program(make_email(sender, body, subject))

    def assertDecision(self, decision, action, rule_name):
        self.assertIs(decision.action, action)
        self.assertEqual(decision.rule.name, rule_name)

    # --- the three rules from the assignment -------------------------------------
    def test_allowed_domain_is_not_spam_even_with_many_bad_words(self):
        decision = self.decide("news@trusted.example", " ".join([SIX_BAD_WORDS] * 3))
        self.assertDecision(decision, Action.MOVE_TO_EMAIL, "ALLOW_LIST")
        self.assertEqual(decision.state.bad_word_count, 18)

    def test_restricted_domain_is_spam_even_with_no_bad_words(self):
        decision = self.decide("friend@spam.test", "Lunch on Thursday?")
        self.assertDecision(decision, Action.MOVE_TO_SPAM, "RESTRICT_LIST")
        self.assertEqual(decision.state.bad_word_count, 0)

    def test_more_than_five_bad_words_is_spam(self):
        self.assertDecision(self.decide("x@unknown.example", SIX_BAD_WORDS),
                            Action.MOVE_TO_SPAM, "BAD_WORDS")

    def test_exactly_five_bad_words_is_not_spam(self):
        decision = self.decide("x@unknown.example", FIVE_BAD_WORDS)
        self.assertEqual(decision.state.bad_word_count, BAD_WORD_THRESHOLD)
        self.assertDecision(decision, Action.MOVE_TO_EMAIL, "DEFAULT")

    def test_clean_email_from_unknown_domain_is_not_spam(self):
        self.assertDecision(self.decide("x@unknown.example", "See you at the lab."),
                            Action.MOVE_TO_EMAIL, "DEFAULT")

    # --- how bad words are counted ------------------------------------------------
    def test_repeated_word_counts_every_occurrence(self):
        decision = self.decide("x@unknown.example", "free " * 6)
        self.assertEqual(decision.state.bad_word_hits, {"free": 6})
        self.assertIs(decision.action, Action.MOVE_TO_SPAM)

    def test_case_and_punctuation_do_not_hide_bad_words(self):
        decision = self.decide("x@unknown.example", "FREE!!! Cash... PRIZE?? Winner; LOTTERY, bonus.")
        self.assertEqual(decision.state.bad_word_count, 6)
        self.assertIs(decision.action, Action.MOVE_TO_SPAM)

    def test_only_whole_words_count(self):
        decision = self.decide("x@unknown.example", "freedom cashier prizes winners clicked bonuses")
        self.assertEqual(decision.state.bad_word_count, 0)

    def test_bad_words_in_the_subject_are_not_counted(self):
        decision = self.decide("x@unknown.example", "hello", subject=SIX_BAD_WORDS)
        self.assertDecision(decision, Action.MOVE_TO_EMAIL, "DEFAULT")

    # --- domains -----------------------------------------------------------------
    def test_sub_domains_follow_their_parent_domain(self):
        self.assertDecision(self.decide("it@mail.trusted.example", SIX_BAD_WORDS),
                            Action.MOVE_TO_EMAIL, "ALLOW_LIST")
        self.assertDecision(self.decide("x@promo.spam.test", "hi"),
                            Action.MOVE_TO_SPAM, "RESTRICT_LIST")

    def test_look_alike_domain_gets_no_allow_list_privilege(self):
        self.assertDecision(self.decide("it@fake-trusted.example", SIX_BAD_WORDS),
                            Action.MOVE_TO_SPAM, "BAD_WORDS")

    def test_domain_matching_ignores_case(self):
        self.assertDecision(self.decide("News@TRUSTED.Example", SIX_BAD_WORDS),
                            Action.MOVE_TO_EMAIL, "ALLOW_LIST")

    def test_domain_on_both_lists_follows_rule_order(self):
        both = FilterLists(allow_domains=frozenset({"both.example"}),
                           restrict_domains=frozenset({"both.example"}),
                           bad_words=TEST_LISTS.bad_words)
        decision = SpamFilterAgent(both).program(make_email("a@both.example", "hi"))
        self.assertDecision(decision, Action.MOVE_TO_EMAIL, "ALLOW_LIST")

    # --- missing or malformed input ----------------------------------------------
    def test_unknown_sender_is_judged_on_bad_words_only(self):
        self.assertDecision(self.decide(None, SIX_BAD_WORDS), Action.MOVE_TO_SPAM, "BAD_WORDS")
        self.assertDecision(self.decide(None, "hello"), Action.MOVE_TO_EMAIL, "DEFAULT")
        self.assertDecision(self.decide("not an address", "hello"), Action.MOVE_TO_EMAIL, "DEFAULT")

    def test_empty_email_is_not_spam(self):
        decision = self.agent.program(b"")
        self.assertDecision(decision, Action.MOVE_TO_EMAIL, "DEFAULT")


class TestRuleTable(unittest.TestCase):
    def test_rules_are_in_the_documented_priority_order(self):
        self.assertEqual([r.name for r in RULES],
                         ["ALLOW_LIST", "RESTRICT_LIST", "BAD_WORDS", "DEFAULT"])

    def test_rule_match_returns_first_matching_rule(self):
        agent = SpamFilterAgent(TEST_LISTS)
        state = EmailState("x.example", on_allow_list=True, on_restrict_list=True,
                           bad_word_hits={"free": 10})
        self.assertEqual(agent.rule_match(state).name, "ALLOW_LIST")

    def test_default_rule_always_matches(self):
        state = EmailState(None, on_allow_list=False, on_restrict_list=False, bad_word_hits={})
        self.assertEqual(SpamFilterAgent(TEST_LISTS).rule_match(state).name, "DEFAULT")

    def test_agent_has_no_memory_between_emails(self):
        agent = SpamFilterAgent(TEST_LISTS)
        first = agent.program(make_email("x@unknown.example", "hello"))
        agent.program(make_email("x@spam.test", SIX_BAD_WORDS))
        again = agent.program(make_email("x@unknown.example", "hello"))
        self.assertEqual(first, again)


if __name__ == "__main__":
    unittest.main()
