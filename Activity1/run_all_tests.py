"""Run the test of both questions with the command:  python run_all_tests.py
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SUITES = ["question1_spam_filter", "question2_jug_problem"]


def main() -> int:
    failed = []
    for suite in SUITES:
        print(f"\n===== {suite} =====", flush=True)
        completed = subprocess.run([sys.executable, "-m", "unittest", "discover", "-v"],
                                   cwd=ROOT / suite)
        if completed.returncode != 0:
            failed.append(suite)
    print("\nAll test suites passed." if not failed else f"\nFAILED: {', '.join(failed)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
