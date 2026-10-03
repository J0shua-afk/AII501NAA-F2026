# AII501NAA – Activity 1 – Written Answers

The programming parts (Q1 d and Q2 d) are in the code; see [README.md](README.md) for how to run them. Terminology and figure numbers follow Russell & Norvig, *Artificial Intelligence: A Modern Approach* (AIMA), 4th edition.

---

## Question 1 – Spam Filter Email Agent

### a) PEAS description

| | Spam-filter agent |
|---|---|
| **Performance measure** | Every email ends up in exactly one folder, and it is the right one: mail from an allow-listed domain in `email/`; mail from a restrict-listed domain in `spam/`; otherwise mail with more than 5 bad-word occurrences in its readable body in `spam/`; all other mail in `email/`. No email is lost, duplicated or altered. A malformed or unreadable email never stops the other emails from being processed. Measured as the fraction of emails placed in the correct folder. |
| **Environment** | An inbox folder of `.eml` files (headers + body; bodies may be multipart MIME, base64 or quoted-printable encoded, HTML, contain text attachments, non-text attachments, or be malformed); the allow list, restrict list and bad-word list files; the `spam/` and `email/` destination folders on the file system. Indirectly, the people and programs that send the emails, spammers included. |
| **Actuators** | A file-system operation that places the current email in `spam/` or in `email/` (copy by default, move with `--move`). These are the agent's only two actions: `MOVE_TO_SPAM` and `MOVE_TO_EMAIL`. (The console report of what was done is output for the user, not a way of changing the environment.) |
| **Sensors** | Reading a file from the inbox: each percept is the complete raw content of one `.eml` file (all headers, the body and every attachment). The three list files are read once at start-up and become the agent's fixed knowledge. Decoding the raw text (MIME parsing, base64/quoted-printable, character sets, HTML) is not a sensor: it is the agent program's INTERPRET-INPUT step. |

### b) Properties of the task environment

| Property | Classification | Reason |
|---|---|---|
| Observable | **Fully observable** (effectively) | AIMA calls an environment effectively fully observable when the sensors detect every aspect *relevant to the choice of action*. Every rule depends only on the sender's domain and the readable body text, and both are inside the percept (the email file). *Caveat:* with respect to whether an email is "really" spam, the environment is partially observable: the From header can be forged, and encrypted or binary content cannot be read. The assignment defines correct behaviour in terms of what is visible, so for this task it is fully observable. |
| Agents | **Single-agent** | Only the filter makes decisions while the program runs. In the real world, spammers adapt their emails to get past filters (a competitive multi-agent situation), but here the emails and lists are fixed input that does not react to the agent. |
| Deterministic / nondeterministic | **Deterministic** | The next state is completely determined by the current state and the action: placing a file in `spam/` or `email/` always puts it there, and the same email with the same lists always gets the same decision. |
| Episodic / sequential | **Episodic** | Each email is one episode: perceive one email, take one action. The decision about one email does not affect any later email, so the agent needs no memory (AIMA's assembly-line inspection example works the same way). |
| Static / dynamic | **Static** | Nothing changes while the agent is deciding: the email file and the lists stay the same, and there is no time pressure. (A live mail server would receive new mail during a run, but new arrivals do not change the right decision for the current email.) |
| Discrete / continuous | **Discrete** | There is a finite number of emails, each a finite string of characters, and exactly two actions. |
| Known / unknown | **Known** | The rules of the environment are given: the assignment states exactly when an email is spam, and the outcome of each action is known in advance. |

### c) Most appropriate agent type: a simple reflex agent

A **simple reflex agent** (AIMA Figure 2.10) chooses its action from the *current percept only*, using condition–action rules:

```
function SIMPLE-REFLEX-AGENT(percept) returns an action
    persistent: rules, a set of condition–action rules
    state  ← INTERPRET-INPUT(percept)
    rule   ← RULE-MATCH(state, rules)
    action ← rule.ACTION
    return action
```

This structure is the best fit, for these reasons:

1. **The assignment literally specifies condition–action rules.** "If the domain is on the allow list → not spam", "if the domain is on the restrict list → spam", "if more than 5 bad words → spam". These translate directly into an ordered rule table:

   | # | Condition (on the interpreted email) | Action |
   |---|---|---|
   | 1 | sender domain is on the allow list | move to `email/` |
   | 2 | sender domain is on the restrict list | move to `spam/` |
   | 3 | more than 5 bad-word occurrences in the body | move to `spam/` |
   | 4 | otherwise | move to `email/` |

   The rule order is the conflict-resolution strategy: RULE-MATCH returns the first rule that matches, so rule 1 overrides everything ("regardless of its contents"), and rule 3 only applies when the sender is on neither list, exactly as the assignment states.

2. **The correct action depends only on the current percept.** The decision for an email is a function of that email's sender domain and body. AIMA notes that a simple reflex agent works only if the correct decision can be made from the current percept alone, i.e. when the environment is (effectively) fully observable; part (b) shows this holds.

3. **No internal state is needed.** The environment is episodic, so there is nothing to remember between emails. A **model-based reflex agent** would add a model of how the world evolves that would never be used.

4. **No planning is needed.** One action per email achieves the outcome immediately, so there is no sequence of actions to search for. A **goal-based agent** adds search/planning machinery for nothing.

5. **No trade-offs need weighing.** The rules already define the correct outcome; there are no degrees of preference between outcomes for a utility function to compare. (The one conflict, a domain on both lists, is settled by rule order; see the README's assumptions.) A **utility-based agent** is unnecessary.

6. **No learning is required.** The lists are supplied and fixed. A real-world spam filter would be a **learning agent** (for example a naive-Bayes classifier that improves from user feedback), but that goes beyond what this assignment specifies.

The agent is **rational** in AIMA's sense: for every percept it takes the action that maximises the performance measure defined in (a), given the percept and its built-in knowledge (the three lists). It is also transparent: every decision can be traced to the single rule that fired, which the program prints.

### d) Implementation

See `question1_spam_filter/`. `spam_agent/agent.py` follows the SIMPLE-REFLEX-AGENT pseudocode line by line; `spam_agent/environment.py` provides the sensor and actuator.

---

## Question 2 – Three-Jug Search Problem

### a) States, actions and transition model

**State representation.** A triple **(a, b, c)** of integers: the gallons currently in the 12-, 8- and 3-gallon jugs, with 0 ≤ a ≤ 12, 0 ≤ b ≤ 8, 0 ≤ c ≤ 3. That gives 13 × 9 × 4 = 468 possible triples, of which **314 are reachable** from the initial state. (These are exactly the triples in which at least one jug is empty or full, because every action ends with some jug empty or full.)

The triple is a sufficient description: the faucet supplies unlimited water and the ground absorbs any amount, so neither needs tracking. The jugs have no markings, so a jug can only be filled to the top, emptied completely, or poured until the source is empty or the destination is full. Every action therefore produces whole-gallon amounts, and what can happen next depends only on the current contents.

- **Initial state:** (0, 0, 0), all jugs empty.
- **Goal states:** any state in which some jug holds exactly one gallon: { (a, b, c) | a = 1 or b = 1 or c = 1 }, e.g. (1, 8, 3) or (0, 8, 1). The measured gallon is then sitting in that jug.
- **Actions** (12 in total), each applicable only when it would change the state:

  | Action | Meaning | Applicable when |
  |---|---|---|
  | Fill(i), i ∈ {12, 8, 3} | fill jug i to the top from the faucet | jug i is not full |
  | Empty(i) | pour all of jug i onto the ground | jug i is not empty |
  | Pour(i, j), i ≠ j | pour jug i into jug j until i is empty or j is full | jug i is not empty and jug j is not full |

  Leaving out actions that change nothing (filling a full jug, for example) removes useless self-loops without losing any solution.

- **Transition model** RESULT(s, a), with capacity Cap(i):
  - Fill(i): jug i becomes Cap(i).
  - Empty(i): jug i becomes 0.
  - Pour(i, j): let t = min(s[i], Cap(j) − s[j]); jug i becomes s[i] − t and jug j becomes s[j] + t.
  - All other jugs are unchanged. Example: RESULT((12, 0, 0), Pour(12→8)) = (4, 8, 0).
- **Action cost:** 1 per action, so the path cost is the number of steps.

### b) Does a heuristic function make sense?

**A heuristic can be defined, but it adds very little here**, for three reasons:

1. **The state space is tiny.** Only 314 states are reachable, and the shortest solution is 3 actions long. BFS finds it after expanding 7 nodes, so there is almost nothing left for a heuristic to save.
2. **"Numerical closeness" is misleading.** The obvious idea, "how close is some jug to 1 gallon?", does not measure the number of actions remaining, because actions move water in large jumps rather than one gallon at a time. For example, (2, 0, 0) has a jug only 1 gallon away from the target but needs **3** more actions, (0, 0, 2) needs **4**, while (12, 0, 0), which looks far away, needs only **2**.
3. **The solution is short.** The farthest reachable state is only 5 actions from a goal, so any admissible heuristic has very little room to separate good states from bad ones.

A sensible heuristic is a **one-step look-ahead**:

- **h = 0** if some jug already holds exactly 1 gallon;
- **h = 1** if a single pour would leave exactly 1 gallon in the source jug (the source holds exactly one gallon more than the free space in the target, e.g. (4, 8, 0): pouring the 12-gallon jug into the empty 3-gallon jug leaves 1);
- **h = 2** otherwise.

This heuristic never overestimates (each value is a true lower bound on the remaining number of actions), so it is admissible. It is also consistent. Both properties were checked by computer against the true distance for all 314 reachable states. With A\* it would find the same 3-action solution while expanding slightly fewer nodes. The assignment asks for breadth-first search, an uninformed algorithm, so the heuristic is not used in the implementation.

### c) Is any search algorithm guaranteed to reach a goal state?

**No, not every search algorithm is guaranteed to reach a goal, although a goal state is reachable and every *complete* algorithm will find it.**

- **A goal is reachable.** The sequence Fill(12), Pour(12→8), Pour(12→3) reaches (1, 8, 3). More generally, because gcd(12, 8, 3) = 1, any whole number of gallons up to 12 can be measured (Bézout's identity).
- **The state space is finite** (314 reachable states) and the branching factor is at most 12. Any **systematic graph search** that remembers which states it has reached, such as BFS, uniform-cost search, graph-search DFS, iterative deepening or A\* with an admissible heuristic, can visit each state at most once, so it must reach the goal after a finite number of steps.
- **Not every algorithm is complete, though.** The state space contains cycles (Fill(12) then Empty(12) returns to the start), so:
  - **depth-first tree search** with no record of visited states can go around a cycle forever, e.g. Fill(12), Empty(12), Fill(12), …;
  - **depth-limited search** with a limit below 3 fails, because the shallowest goal is at depth 3;
  - **greedy best-first tree search** and **local search** (hill climbing) can loop or get stuck on plateaus.
- **BFS is complete and optimal here.** It is complete because the branching factor is finite and the goal is at a finite depth. It is optimal because every action costs 1, so the first goal it generates is at the smallest depth: it returns a 3-action solution, and no solution with fewer actions exists.

If the goal were unreachable (for example jugs of 4 and 2 gallons, where only even amounts are possible), a complete graph search would still **terminate**: it explores all reachable states and reports failure. The implementation does exactly this (`python main.py --capacities 4 2 --goal 1`).

### d) Implementation

See `question2_jug_problem/`. `jug_search/search.py` contains `breadth_first_search`, a line-by-line implementation of AIMA Figure 3.9, together with Node and EXPAND (Figure 3.7). `jug_search/jug_problem.py` contains the problem formulation from part (a).
