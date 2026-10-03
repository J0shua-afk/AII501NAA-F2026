"""Spam-filter agent for AII501NAA Activity 1, Question 1.

Modules, in the order the data flows through them:

    environment.py   the inbox and the spam/ + email/ folders (sensor and actuator)
    agent.py         the SIMPLE-REFLEX-AGENT: interpret the percept, match a rule, act
    email_parser.py  reads an .eml file: sender domain + readable body text
    lists.py         loads the allow list, restrict list and bad-word list
    text_utils.py    shared helpers: word tokenizer, domain normalising/matching
"""
