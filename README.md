# Spam-Filter-Email-Agent
# AII501NAA – Activity 1

Two Python programs for Activity 1:

1. **Question 1 – Spam Filter Email Agent.** A *simple reflex agent* that reads `.eml` email files and files each one into a `spam/` or an `email/` directory, using an allow list, a restrict list and a bad-word list.
2. **Question 2 – Three-Jug Search Problem.** The 12/8/3-gallon jug problem formulated as a search problem and solved with breadth-first search.
**The written answers** (PEAS, environment properties, agent type, state space, heuristic, completeness) are in **[ANSWERS.md](ANSWERS.md)**.

## Contents

1. [Requirements implemented](#1-requirements-implemented)
2. [Setup](#2-setup)
3. [Running Question 1](#3-running-question-1--spam-filter)
4. [Running Question 2](#4-running-question-2--jug-problem)
5. [Running the tests](#5-running-the-tests)
6. [Project structure](#6-project-structure)
7. [Assumptions](#7-assumptions)
8. [Design decisions](#8-design-decisions)
9. [How the spam-filter agent works](#9-how-the-spam-filter-agent-works)
10. [How the jug problem is represented](#10-how-the-jug-problem-is-represented)
11. [How breadth-first search works](#11-how-breadth-first-search-works)
12. [Testing strategy](#12-testing-strategy)
13. [Use of AI tools](#13-use-of-ai-tools)

---

## 1. Requirements implemented

| Assignment requirement | Where it is implemented |
|---|---|
| Q1 a) PEAS | [ANSWERS.md](ANSWERS.md#a-peas-description) |
| Q1 b) task-environment properties | [ANSWERS.md](ANSWERS.md#b-properties-of-the-task-environment) |
| Q1 c) agent type, with justification | [ANSWERS.md](ANSWERS.md#c-most-appropriate-agent-type-a-simple-reflex-agent) |
| Q1 d) rational agent in the book's form | `question1_spam_filter/spam_agent/agent.py` (SIMPLE-REFLEX-AGENT, Fig. 2.10) |
| Allow-listed domain → non-spam regardless of contents | rule `ALLOW_LIST` (first rule in `agent.py`) |
| Restrict-listed domain → spam regardless of contents | rule `RESTRICT_LIST` |
| More than 5 bad words in the body (and not allow-listed) → spam | rule `BAD_WORDS` (`BAD_WORD_THRESHOLD = 5`) |
| `.eml` = headers + body; text attachments are readable | `spam_agent/email_parser.py` |
| Spam → spam directory, others → email directory | `spam_agent/environment.py` (`execute_action`) |
| Q2 a) states, actions, transition model | [ANSWERS.md](ANSWERS.md#a-states-actions-and-transition-model), `question2_jug_problem/jug_search/jug_problem.py` |
| Q2 b) heuristic | [ANSWERS.md](ANSWERS.md#b-does-a-heuristic-function-make-sense) |
| Q2 c) is a goal guaranteed? | [ANSWERS.md](ANSWERS.md#c-is-any-search-algorithm-guaranteed-to-reach-a-goal-state) |
| Q2 d) breadth-first search as in Figure 3.9 | `question2_jug_problem/jug_search/search.py` (`breadth_first_search`) |
| Source code, test cases, test data, documentation | this folder (102 automated tests) |

## 2. Setup

- **Python 3.10 or newer.** Check with `python --version` (on macOS/Linux the command may be `python3`; on Windows, `py` also works).
- **No packages to install.** Everything uses the Python standard library; `requirements.txt` documents this. Running `pip install -r requirements.txt` is harmless but not needed.

```bash
git clone <your-repository-url>
cd AII501NAA-F2026/Activity1
```

## 3. Running Question 1 – spam filter

```bash
cd question1_spam_filter
python main.py
```

The agent reads every `.eml` file in `data/inbox/`, decides spam or not spam, and **copies** each email into `output/spam/` or `output/email/`. The inbox is left untouched, so the demo can be re-run. Use `--move` to *move* the files out of the inbox, the way a real filter would.

| Option | Default | Meaning |
|---|---|---|
| `--inbox DIR` | `data/inbox` | folder containing the `.eml` files |
| `--output DIR` | `output` | folder in which `spam/` and `email/` are created |
| `--allow-list FILE` | `data/allow_list.txt` | allow list (one domain per line) |
| `--restrict-list FILE` | `data/restrict_list.txt` | restrict list (one domain per line) |
| `--bad-words FILE` | `data/bad_words.txt` | bad-word list (one word per line) |
| `--move` | off | move instead of copy |

List files: one entry per line, `#` starts a comment, blank lines are ignored, and case does not matter. Exit codes: `0` = success, `1` = some emails could not be processed (they are reported and left in the inbox), `2` = a list file or the inbox is missing.

**Example output** (sample data):

```
Spam filter agent: 14 email(s) in data/inbox (copy mode)
Lists: 3 allowed domains, 3 restricted domains, 31 bad words
Rules, checked in order: ALLOW_LIST -> email | RESTRICT_LIST -> spam | BAD_WORDS (more than 5) -> spam | DEFAULT -> email

FILE                               SENDER DOMAIN              BAD WORDS  RULE           FOLDER
01_normal_email.eml                mailbox.example                    0  DEFAULT        email
02_allow_list_newsletter.eml       university.example                 8  ALLOW_LIST     email
03_allow_list_subdomain.eml        helpdesk.employer.example          6  ALLOW_LIST     email
04_restrict_list_no_bad_words.eml  spammer.test                       0  RESTRICT_LIST  spam
05_lottery_scam.eml                winners-circle.test                7  BAD_WORDS      spam
06_exactly_five_bad_words.eml      mailbox.example                    5  DEFAULT        email
07_six_bad_words_mixed_case.eml    shopping-promos.test               6  BAD_WORDS      spam
08_same_word_repeated.eml          random-shop.test                   6  BAD_WORDS      spam
09_text_attachment.eml             mailbox.example                    8  BAD_WORDS      spam
10_html_and_plain_versions.eml     student-club.example               4  DEFAULT        email
11_base64_encoded_body.eml         online-billing.test                8  BAD_WORDS      spam
12_lookalike_domain.eml            my-university.example              7  BAD_WORDS      spam
13_missing_from_header.eml         (unknown)                          0  DEFAULT        email
14_malformed_from_header.eml       (unknown)                          7  BAD_WORDS      spam

Result: 8 spam, 6 email, 0 error(s)
Spam folder:  output/spam
Email folder: output/email
```

What each sample email demonstrates:

| Email | Demonstrates |
|---|---|
| 01 | an ordinary email → not spam |
| 02, 03 | allow list beats 8 and 6 bad words; 03 is a **sub-domain** of an allowed domain |
| 04 | restrict list beats a perfectly clean email |
| 05 | more than 5 bad words → spam |
| 06 / 07 | the threshold: **exactly 5 → not spam**, **6 → spam**; 07 also mixes case and punctuation (`FREE!!!`, `Click-here;`) |
| 08 | the same word six times counts as 6 |
| 09 | words in a **text attachment** count; the PNG attachment is skipped |
| 10 | plain-text + HTML versions of the same message are counted **once** (4, not 8) |
| 11 | a **base64-encoded** body is decoded before counting |
| 12 | a look-alike domain (`my-university.example`) gets **no** allow-list privilege |
| 13, 14 | missing / malformed `From:` → sender unknown, judged on bad words alone |

## 4. Running Question 2 – jug problem

```bash
cd question2_jug_problem
python main.py
```

**Example output:**

```
Water-jug problem - breadth-first search (AIMA Figure 3.9)
Jugs:          12-gallon jug, 8-gallon jug, 3-gallon jug
Initial state: (0, 0, 0)
Goal:          any jug holds exactly 1 gallon

Step  Action                                        12-gal   8-gal   3-gal
   0  (initial state)                                    0       0       0
   1  Fill the 12-gallon jug from the faucet            12       0       0
   2  Pour the 12-gallon jug into the 8-gallon jug       4       8       0
   3  Pour the 12-gallon jug into the 3-gallon jug       1       8       3

Goal reached after 3 actions: the 12-gallon jug holds exactly 1 gallon.
BFS expanded 7 nodes and generated 33. Every action costs 1, so this is a shortest solution.
```

Other jugs and goals can be tried with `--capacities` and `--goal`. An unsolvable case shows how failure is reported:

```
$ python main.py --capacities 4 2 --goal 1
...
No solution: no sequence of actions leaves exactly 1 gallon in a jug.
BFS expanded all 6 reachable states before reporting failure.
```

## 5. Running the tests

Both suites from the `Activity1` folder:

```bash
python run_all_tests.py
```

Or each question on its own, from inside its folder:

```bash
cd question1_spam_filter && python -m unittest discover -v
cd question2_jug_problem && python -m unittest discover -v
```

Current result: **68 tests (Question 1) + 34 tests (Question 2), all passing.**

## 6. Project structure

```
Activity1/
├── README.md                      this file
├── ANSWERS.md                     written answers: Q1 a–c, Q2 a–c
├── requirements.txt               no third-party packages (standard library only)
├── run_all_tests.py               runs both test suites
├── question1_spam_filter/
│   ├── main.py                    command-line entry point
│   ├── spam_agent/                the agent (source code)
│   │   ├── agent.py               SIMPLE-REFLEX-AGENT: rules, RULE-MATCH, INTERPRET-INPUT
│   │   ├── environment.py         inbox + spam/ + email/: sensor and actuator
│   │   ├── email_parser.py        .eml parsing: sender domain, readable body text
│   │   ├── lists.py               loads the allow, restrict and bad-word lists
│   │   └── text_utils.py          tokenizer, domain normalising and matching
│   ├── data/                      sample data for the demo
│   │   ├── allow_list.txt, restrict_list.txt, bad_words.txt
│   │   └── inbox/                 14 sample .eml files
│   └── tests/                     unit, integration and end-to-end tests
│       └── fixtures/              test-only .eml and list files
└── question2_jug_problem/
    ├── main.py                    command-line entry point
    ├── jug_search/
    │   ├── search.py              generic: Problem, Node, EXPAND, breadth_first_search
    │   └── jug_problem.py         the jug problem: states, actions, RESULT, goal test
    └── tests/                     formulation and BFS tests
```

`question1_spam_filter/output/` is created when the agent runs and is ignored by git.

## 7. Assumptions

The assignment is the authority. Where it is silent or ambiguous, the choices below were made. Each is documented here and covered by a test.

**Stated explicitly in the assignment**

- Allow-listed domain → non-spam regardless of contents; restrict-listed domain → spam regardless of contents.
- More than 5 bad words in the body, and not from an allow-listed domain → spam.
- Text attachments are readable by the agent. Spam goes to a spam directory and everything else to an email directory.
- Three jugs of 12, 8 and 3 gallons and a faucet; jugs can be filled, emptied onto the ground or poured into one another; the goal is exactly one gallon; BFS as in Figure 3.9.

**Reasonable assumptions where the assignment is silent or ambiguous (Question 1)**

1. **Restrict list wording.** The assignment says the restrict list "lists safe domains". Since its emails are classified as spam, this is read as a typo for *unsafe* domains.
2. **"Coming from that domain"** means the domain of the address in the `From:` header, compared case-insensitively. The display name is ignored (`"support@bank.example" <thief@evil.test>` comes from `evil.test`).
3. **Sub-domains belong to their domain.** `helpdesk.employer.example` matches a listed `employer.example`. Matching only happens at a dot boundary, so `my-university.example` does **not** match `university.example`.
4. **A missing, malformed or ambiguous `From:` header** (no address, or more than one) means the sender is *unknown*. An unknown sender can never be on either list, so it is judged on bad words alone.
5. **"More than 5 words … found on this list"** counts *every occurrence*: "free" six times is 6, so the email is spam. Exactly 5 is not spam. (The other possible reading, counting only *distinct* bad words, is noted under design decisions.)
6. **A "word"** is a run of letters/digits; case and punctuation are ignored (`FREE!!!` = `free`), and only whole words count (`freedom` is not `free`).
7. **"Body"** means all readable text: `text/plain` and `text/html` parts (HTML tags, scripts and styles removed), including text attachments. Base64 and quoted-printable encodings and character sets are decoded. Non-text parts (images, PDFs, …) cannot be read and are skipped. When the same content appears in several formats (`multipart/alternative`), only one version is read, so words are not double counted. **The subject line is a header, not part of the body**, so it is not counted.
8. **A domain on both lists** goes to `email/`. The allow rule is checked first, because wrongly hiding a legitimate email is the more costly mistake. The program prints a warning when it detects this conflict.
9. **Bad-word list entries must be single words.** An entry such as `click here` or `$$$` cannot match a single word and is skipped with a warning.
10. **An email that cannot be processed** (unreadable file, unexpected error) is left in the inbox and reported. It is never guessed into a folder.

**Reasonable assumptions (Question 2)**

1. All jugs start empty, the faucet is unlimited, and the jugs have no markings (so only fill / empty / pour-until-full-or-empty are possible).
2. "Measure out exactly one gallon" means **some jug contains exactly 1 gallon**.
3. Every action costs 1.
4. Actions that would not change the state (filling a full jug, pouring from an empty one) are not applicable.

## 8. Design decisions

- **Simple reflex agent, written in the book's form.** `SpamFilterAgent.program()` contains the three lines of AIMA's SIMPLE-REFLEX-AGENT: `interpret_input`, then `rule_match`, then `rule.action`. The rules are data (the `RULES` table), so their order, and therefore their priority, can be seen at a glance. See [ANSWERS.md](ANSWERS.md#c-most-appropriate-agent-type-a-simple-reflex-agent) for why this agent type fits.
- **The agent program returns a `Decision`.** It contains the action, plus the rule that fired and the facts it saw, so the program can explain every decision. Only the action is used by the actuator, and nothing is fed back into the agent, which has no memory between emails.
- **Sensor and actuator live in `MailEnvironment`**, separate from the agent program, mirroring PEAS: the environment reads files (sensor) and places files (actuator); the agent only maps percept → action.
- **One tokenizer for both sides.** The same `tokenize()` processes the bad-word list and the email body, so they always agree on what a word is. Similarly, one `normalize_domain()` handles list entries and sender addresses.
- **Copy by default, `--move` optional.** Copying keeps the sample inbox intact, so the demo and the tests are repeatable. In move mode an existing file is never overwritten (`name_1.eml` is used instead), so no email can be lost.
- **Deterministic.** Emails are processed in alphabetical order; jug actions are generated in a fixed order (fills, empties, pours), so BFS always returns the same solution.
- **Standard library only.** `email` parses `.eml`/MIME, `html.parser` strips HTML, `unittest` runs the tests. Nothing needs installing.
- **Occurrences vs. distinct words.** Counting occurrences follows the wording "more than 5 words within the body". To count distinct words instead, one line in `agent.py` would change: replace `sum(self.bad_word_hits.values())` with `len(self.bad_word_hits)`.
- **BFS mirrors Figure 3.9 line by line**, with the pseudocode in the docstring and as end-of-line comments. `Problem`, `Node` and `expand` are kept generic (they know nothing about jugs), and a test runs the same BFS on a small graph to show this.
- **`reached` instead of "explored".** The 4th-edition Figure 3.9 uses one set, `reached`, holding every state ever added to the frontier. It does the job of the 3rd edition's "explored set + frontier check", so no state is queued twice.
- **Goal test on generation (early goal test).** Figure 3.9 tests each child as soon as it is generated rather than when it is popped. With unit action costs this still returns a shortest solution and saves a whole layer of expansions.

## 9. How the spam-filter agent works

For each `.eml` file in the inbox, `MailEnvironment.run()` performs one perceive → decide → act cycle:

```
sensor          percept = raw bytes of the .eml file              (environment.py)
   │
agent program   state  = interpret_input(percept)                 (agent.py)
   │                ├─ parse_email(): From address → domain;      (email_parser.py)
   │                │   text parts + text attachments → body text
   │                └─ facts: on_allow_list? on_restrict_list?
   │                          bad_word_hits (word → count)
   │            rule   = rule_match(state): first rule that holds
   │            action = rule.action
   │
actuator        place the file in output/spam/ or output/email/   (environment.py)
```

**How the three list rules interact.** RULE-MATCH tries the rules in order and stops at the first match:

1. `ALLOW_LIST`: sender domain on the allow list → `email/`. Nothing else is looked at; this is what "regardless of its contents" means.
2. `RESTRICT_LIST`: sender domain on the restrict list → `spam/`.
3. `BAD_WORDS`: more than 5 bad-word occurrences in the body → `spam/`. Reaching this rule already means the sender is not allow-listed, exactly as the assignment's bad-word rule requires.
4. `DEFAULT`: everything else → `email/`.

**How PEAS maps to the code:** *Performance measure* → the expected folder for every sample email, checked by the end-to-end test; *Environment* → `data/inbox`, the list files and `output/`; *Actuators* → `MailEnvironment.execute_action`; *Sensors* → `MailEnvironment.percept`.

**How email parsing works.** Python's `email` package splits the file into headers and a tree of MIME parts. `email_parser.py` then:

- takes the single address in `From:` and keeps the text after its last `@` as the domain;
- walks the MIME tree, decoding every `text/*` part (base64 or quoted-printable, then the declared character set, falling back to UTF-8 for unknown charsets);
- strips HTML down to its visible text;
- picks one version of each `multipart/alternative`;
- skips non-text parts.

## 10. How the jug problem is represented

A state is a tuple `(a, b, c)`: gallons in the 12-, 8- and 3-gallon jugs. The start is `(0, 0, 0)`; any state containing a `1` is a goal. `JugProblem` provides the four parts BFS needs:

- `is_goal(s)`: `1 in s`.
- `actions(s)`: every applicable action, from a fixed list of 12 (Fill ×3, Empty ×3, Pour ×6). An action is applicable only if it changes the state.
- `result(s, a)`, the transition model:
  - Fill: the jug becomes full.
  - Empty: the jug becomes 0.
  - Pour i→j: move `min(s[i], capacity[j] − s[j])` gallons from i to j.

  Calling `result` with an inapplicable action raises `ValueError`.
- `action_cost`: 1 for every action (inherited from `Problem`).

**Successor generation.** `expand(problem, node)` (Figure 3.7) asks `problem.actions(state)` for the applicable actions and builds one child `Node` per action, recording the parent, the action and the path cost. The solution is read back by following parent links from the goal node (`path_states`, `path_actions`).

## 11. How breadth-first search works

BFS always expands the **shallowest** unexpanded node first, because the frontier is a FIFO queue: new nodes join at the back and nodes are taken from the front. The `reached` set stops any state from being queued twice, and each child is goal-tested as soon as it is generated.

The actual run, step by step (from an instrumented copy of the same code):

| # | Node expanded (popped from the front) | Children added to the frontier (already-reached states are skipped) |
|---|---|---|
| 1 | (0, 0, 0) | (12, 0, 0), (0, 8, 0), (0, 0, 3) |
| 2 | (12, 0, 0) | (12, 8, 0), (12, 0, 3), (4, 8, 0), (9, 0, 3) |
| 3 | (0, 8, 0) | (0, 8, 3), (8, 0, 0), (0, 5, 3) |
| 4 | (0, 0, 3) | (3, 0, 0), (0, 3, 0) |
| 5 | (12, 8, 0) | (12, 8, 3), (9, 8, 3), (12, 5, 3) |
| 6 | (12, 0, 3) | (4, 8, 3), (12, 3, 0) |
| 7 | (4, 8, 0) | (4, 0, 0), then **(1, 8, 3): goal, returned immediately** |

Expansions 1–4 cover depths 0–1; expansion 7 is the first depth-2 node whose children include a goal. The solution is found at depth 3. Following parent links back from (1, 8, 3) gives Fill(12) → Pour(12→8) → Pour(12→3). Because BFS finishes every depth before starting the next, no shorter solution exists; a test confirms this independently by brute force.

**Goal detection.** `is_goal` is called on the initial state, then on every generated child. If the frontier empties without finding a goal, BFS returns `None` (failure), which `main.py` reports.

## 12. Testing strategy

| Test file | What it checks |
|---|---|
| `question1_spam_filter/tests/test_text_and_lists.py` | tokenizer (case, punctuation, whole words); domain normalising; sub-domain vs look-alike matching; list loading (comments, duplicates, case, `@`/`*.` prefixes, Windows BOM, invalid entries, missing file); conflict warning |
| `…/tests/test_email_parser.py` | `From:` extraction (display names, spoofing tricks, missing/malformed headers); body extraction (text attachments read, PDF skipped, alternative read once, HTML stripped, base64 and quoted-printable decoded, broken MIME, unknown charset, forwarded message, empty file); subject not counted |
| `…/tests/test_agent.py` | each rule and their priority; threshold boundary (5 vs 6); repeated words; case/punctuation; sub-domains; domain on both lists; unknown senders; rule-table order; no memory between emails |
| `…/tests/test_environment.py` | copy/move placement; never overwriting; re-runs keep each email in one folder; ignoring non-`.eml` files; errors reported without stopping the run; **end-to-end run on all 14 sample emails**; command-line exit codes |
| `question2_jug_problem/tests/test_jug_problem.py` | initial state; goal test; actions in empty/full/mixed states; each transition; capacity limits and water conservation over all 314 reachable states; invalid actions rejected |
| `…/tests/test_bfs.py` | solution found and holds exactly 1 gallon; every step legal; the exact 3-step path; brute-force proof that no shorter path exists; deterministic; initial-state goal; failure reported (4/2 jugs, unreachable goal); **no state expanded twice**; breadth-first expansion order; BFS on a generic graph; EXPAND builds correct nodes |

Test data lives outside the source code: `question1_spam_filter/data/` (demo inbox and lists) and `question1_spam_filter/tests/fixtures/` (test-only emails and lists).

## 13. Use of AI tools

An AI assistant (Claude, by Anthropic) was used while developing this activity, to Debug and fix  code, test code, reading code inorder to contribute to drafting a README.
