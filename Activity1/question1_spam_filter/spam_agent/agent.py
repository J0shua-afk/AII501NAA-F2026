"""The spam-filter agent - a SIMPLE REFLEX AGENT (Russell & Norvig, AIMA, Ch. 2, Fig. 2.10).

    function SIMPLE-REFLEX-AGENT(percept) returns an action
        persistent: rules, a set of condition-action rules
        state  <- INTERPRET-INPUT(percept)
        rule   <- RULE-MATCH(state, rules)
        action <- rule.ACTION
        return action

How the pseudocode maps onto this file
--------------------------------------
percept          the raw bytes of ONE .eml file (handed over by MailEnvironment)
INTERPRET-INPUT  SpamFilterAgent.interpret_input():  bytes -> EmailState
rules            RULES: four condition-action rules, checked in order
RULE-MATCH       SpamFilterAgent.rule_match():  the first rule whose condition holds
rule.ACTION      Action.MOVE_TO_SPAM or Action.MOVE_TO_EMAIL

The agent keeps no memory between emails: each decision depends only on the
current percept plus the fixed lists. That is what makes it a *simple* reflex agent.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Optional

from .email_parser import parse_email
from .lists import FilterLists
from .text_utils import domain_matches, tokenize

#: "If MORE THAN 5 words ... are found on this list" -> spam needs 6 or more.
BAD_WORD_THRESHOLD = 5

#: A percept is the complete raw content of one .eml file.
Percept = bytes


class Action(Enum):
    """The agent's two possible actions. The value is the destination folder name."""

    MOVE_TO_SPAM = "spam"
    MOVE_TO_EMAIL = "email"


@dataclass(frozen=True)
class EmailState:
    """INTERPRET-INPUT's description of one email: exactly the facts the rules test."""

    sender_domain: Optional[str]  # None when the From header is missing or malformed
    on_allow_list: bool
    on_restrict_list: bool
    bad_word_hits: Counter        # bad word -> how many times it occurs in the body

    @property
    def bad_word_count(self) -> int:
        """Total bad-word occurrences: a word that appears 3 times counts 3 times."""
        return sum(self.bad_word_hits.values())


@dataclass(frozen=True)
class Rule:
    """A condition-action rule:  IF condition(state) THEN action."""

    name: str
    condition: Callable[[EmailState], bool]
    action: Action


#: The rule table, in priority order (RULE-MATCH returns the FIRST rule that matches):
#:   1. allow list  -> email  ("non-spam regardless of its contents"); it is checked
#:      before the restrict list, so it also wins if a domain is on both lists;
#:   2. restrict list -> spam ("spam regardless of its contents");
#:   3. more than BAD_WORD_THRESHOLD bad words in the body -> spam;
#:   4. otherwise -> email.
RULES: tuple[Rule, ...] = (
    Rule("ALLOW_LIST", lambda s: s.on_allow_list, Action.MOVE_TO_EMAIL),
    Rule("RESTRICT_LIST", lambda s: s.on_restrict_list, Action.MOVE_TO_SPAM),
    Rule("BAD_WORDS", lambda s: s.bad_word_count > BAD_WORD_THRESHOLD, Action.MOVE_TO_SPAM),
    Rule("DEFAULT", lambda s: True, Action.MOVE_TO_EMAIL),
)


@dataclass(frozen=True)
class Decision:
    """The action chosen for one percept, plus the rule that fired and the state it
    was matched against. Only ``action`` affects the environment; ``rule`` and
    ``state`` are kept so the program can explain each decision."""

    action: Action
    rule: Rule
    state: EmailState


class SpamFilterAgent:
    """Simple reflex agent that files each email as spam or as normal email."""

    def __init__(self, lists: FilterLists, rules: tuple[Rule, ...] = RULES) -> None:
        self.lists = lists  # persistent knowledge used by INTERPRET-INPUT (never changes)
        self.rules = rules  # persistent condition-action rules (never change)

    def program(self, percept: Percept) -> Decision:
        """The agent program, SIMPLE-REFLEX-AGENT(percept)."""
        state = self.interpret_input(percept)  # state  <- INTERPRET-INPUT(percept)
        rule = self.rule_match(state)          # rule   <- RULE-MATCH(state, rules)
        return Decision(rule.action, rule, state)  # action <- rule.ACTION; return action

    def interpret_input(self, percept: Percept) -> EmailState:
        """INTERPRET-INPUT: parse the email and compute the facts the rules test."""
        parsed = parse_email(percept)
        words = tokenize(parsed.body_text)
        return EmailState(
            sender_domain=parsed.sender_domain,
            on_allow_list=domain_matches(parsed.sender_domain, self.lists.allow_domains),
            on_restrict_list=domain_matches(parsed.sender_domain, self.lists.restrict_domains),
            bad_word_hits=Counter(word for word in words if word in self.lists.bad_words),
        )

    def rule_match(self, state: EmailState) -> Rule:
        """RULE-MATCH: return the first rule whose condition is true for ``state``."""
        for rule in self.rules:
            if rule.condition(state):
                return rule
        raise LookupError("no rule matched")  # unreachable while DEFAULT is the last rule
