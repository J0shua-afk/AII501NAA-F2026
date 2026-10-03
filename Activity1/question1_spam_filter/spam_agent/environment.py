"""The task environment: an inbox folder of .eml files plus spam/ and email/ folders.

This is where the agent's SENSOR and ACTUATOR live:

* sensor   - read the raw bytes of one .eml file from the inbox   (``percept``)
* actuator - place that file in <output>/spam or <output>/email   (``execute_action``)

``run`` is the perceive -> decide -> act loop, executed once per email.
"""

from __future__ import annotations

import logging
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from .agent import Action, Decision, SpamFilterAgent

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class FilingResult:
    """What happened to one email file."""

    filename: str
    decision: Optional[Decision] = None  # None if the email could not be processed
    destination: Optional[Path] = None   # where the file was placed
    error: Optional[str] = None          # why it could not be processed


class MailEnvironment:
    """An inbox directory and the two destination directories."""

    def __init__(self, inbox: Path, output_dir: Path, move: bool = False) -> None:
        self.inbox = Path(inbox)
        self.folders = {
            Action.MOVE_TO_SPAM: Path(output_dir) / Action.MOVE_TO_SPAM.value,    # .../spam
            Action.MOVE_TO_EMAIL: Path(output_dir) / Action.MOVE_TO_EMAIL.value,  # .../email
        }
        self.move = move  # False: copy (inbox untouched); True: move out of the inbox

    def pending_emails(self) -> list[Path]:
        """The .eml files waiting in the inbox, in alphabetical (deterministic) order."""
        if not self.inbox.is_dir():
            raise FileNotFoundError(f"inbox directory not found: {self.inbox}")
        return sorted(path for path in self.inbox.iterdir()
                      if path.is_file() and path.suffix.lower() == ".eml")

    def percept(self, email_file: Path) -> bytes:
        """SENSOR: the complete raw content of one email file."""
        return email_file.read_bytes()

    def execute_action(self, email_file: Path, action: Action) -> Path:
        """ACTUATOR: place ``email_file`` in the folder named by ``action``."""
        folder = self.folders[action]
        folder.mkdir(parents=True, exist_ok=True)
        if self.move:
            # The moved file is the only copy, so never overwrite an existing file.
            destination = _unused_path(folder / email_file.name)
            shutil.move(str(email_file), str(destination))
        else:
            # Copy mode: the original stays in the inbox, so the output folders are a
            # view of the latest run. Overwrite any earlier copy and delete a stale
            # copy from the *other* folder, so each email ends up in exactly one folder.
            destination = folder / email_file.name
            shutil.copy2(email_file, destination)
            for other_action, other_folder in self.folders.items():
                if other_action is not action:
                    (other_folder / email_file.name).unlink(missing_ok=True)
        return destination

    def run(self, agent: SpamFilterAgent) -> list[FilingResult]:
        """Perceive -> decide -> act for every email in the inbox.

        One bad email never stops the run: if an email cannot be read, parsed or
        filed, it is left where it is and reported as an error.
        """
        results = []
        for email_file in self.pending_emails():
            try:
                percept = self.percept(email_file)                              # sense
                decision = agent.program(percept)                               # decide
                destination = self.execute_action(email_file, decision.action)  # act
            except Exception as exc:  # report the problem and carry on with the next email
                message = f"{type(exc).__name__}: {exc}"
                logger.error("could not process %s (%s); left in the inbox",
                             email_file.name, message)
                results.append(FilingResult(email_file.name, error=message))
            else:
                results.append(FilingResult(email_file.name, decision, destination))
        return results


def _unused_path(path: Path) -> Path:
    """Return ``path``, or ``name_1.eml``, ``name_2.eml``, ... if it is already taken."""
    candidate, counter = path, 1
    while candidate.exists():
        candidate = path.with_name(f"{path.stem}_{counter}{path.suffix}")
        counter += 1
    return candidate
