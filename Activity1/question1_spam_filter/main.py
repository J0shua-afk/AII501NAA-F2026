"""Command-line entry point for the spam-filter agent (Activity 1, Question 1).

Run from this folder:
    python main.py              # classify data/inbox -> output/spam and output/email
    python main.py --move       # move the files out of the inbox instead of copying them
    python main.py --help       # all options
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from spam_agent.agent import BAD_WORD_THRESHOLD, Action, SpamFilterAgent
from spam_agent.environment import FilingResult, MailEnvironment
from spam_agent.lists import FilterLists, ListFileError

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Rule-based spam filter agent: files each .eml email into spam/ or email/.")
    parser.add_argument("--inbox", type=Path, default=DATA / "inbox",
                        help="folder containing the .eml files (default: data/inbox)")
    parser.add_argument("--output", type=Path, default=HERE / "output",
                        help="folder in which spam/ and email/ are created (default: output)")
    parser.add_argument("--allow-list", type=Path, default=DATA / "allow_list.txt",
                        help="allow list file (default: data/allow_list.txt)")
    parser.add_argument("--restrict-list", type=Path, default=DATA / "restrict_list.txt",
                        help="restrict list file (default: data/restrict_list.txt)")
    parser.add_argument("--bad-words", type=Path, default=DATA / "bad_words.txt",
                        help="bad-word list file (default: data/bad_words.txt)")
    parser.add_argument("--move", action="store_true",
                        help="move the emails out of the inbox instead of copying them")
    return parser.parse_args(argv)


def display(path: Path) -> str:
    """Show ``path`` relative to the current folder when possible (shorter output)."""
    try:
        return str(path.resolve().relative_to(Path.cwd().resolve()))
    except ValueError:
        return str(path)


def print_report(results: list[FilingResult], environment: MailEnvironment,
                 lists: FilterLists) -> None:
    mode = "move" if environment.move else "copy"
    print(f"Spam filter agent: {len(results)} email(s) in {display(environment.inbox)} ({mode} mode)")
    print(f"Lists: {len(lists.allow_domains)} allowed domains, "
          f"{len(lists.restrict_domains)} restricted domains, {len(lists.bad_words)} bad words")
    print(f"Rules, checked in order: ALLOW_LIST -> email | RESTRICT_LIST -> spam | "
          f"BAD_WORDS (more than {BAD_WORD_THRESHOLD}) -> spam | DEFAULT -> email")
    print()

    rows = [("FILE", "SENDER DOMAIN", "BAD WORDS", "RULE", "FOLDER")]
    for result in results:
        if result.error:
            rows.append((result.filename, "-", "-", "ERROR", result.error))
        else:
            state = result.decision.state
            rows.append((result.filename, state.sender_domain or "(unknown)",
                         str(state.bad_word_count), result.decision.rule.name,
                         result.decision.action.value))
    widths = [max(len(row[i]) for row in rows) for i in range(4)]
    for name, domain, count, rule, folder in rows:
        print(f"{name:<{widths[0]}}  {domain:<{widths[1]}}  {count:>{widths[2]}}  "
              f"{rule:<{widths[3]}}  {folder}")

    spam = sum(1 for r in results if r.decision and r.decision.action is Action.MOVE_TO_SPAM)
    errors = sum(1 for r in results if r.error)
    print()
    print(f"Result: {spam} spam, {len(results) - spam - errors} email, {errors} error(s)")
    print(f"Spam folder:  {display(environment.folders[Action.MOVE_TO_SPAM])}")
    print(f"Email folder: {display(environment.folders[Action.MOVE_TO_EMAIL])}")


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")
    args = parse_args(argv)
    try:
        lists = FilterLists.from_files(args.allow_list, args.restrict_list, args.bad_words)
        environment = MailEnvironment(args.inbox, args.output, move=args.move)
        results = environment.run(SpamFilterAgent(lists))
    except (ListFileError, FileNotFoundError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    print_report(results, environment, lists)
    return 1 if any(r.error for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
