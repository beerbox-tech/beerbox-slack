"""commonalities for local scripts"""

import os
import subprocess
from typing import Sequence

LINE_LENGTH = 72


def print_with_state(message: str, state: str, end: str = "\n") -> None:
    """print a message with a state
    message .................................. [state]
    """
    # the 4 are for the space after message and before state
    # and the 2 brackets around the state
    pad = "." * max(0, LINE_LENGTH - len(message) - len(state) - 4)
    color = "\033[46m\033[30m"
    if state == "success":
        color = "\033[42m"
    if state == "failure":
        color = "\033[41m\033[93m"
    colorized_state = f"{color}[{state}]\033[0m"
    print(f"{message} {pad} {colorized_state}", end=end)


def run_with_state(message: str, command: Sequence[str]) -> int:
    """run a command with a given message and update state accordingly
    message .................................. [ongoing]
    [run the command in background]
    message .................................. [success | failure]
    """
    if not os.getenv("CI"):
        print_with_state(message, state="ongoing", end="\r")
    result = subprocess.run(command, capture_output=True, check=False)
    if result.returncode == 0:
        print_with_state(message, state="success", end="\n")
        return 0
    print_with_state(message, state="failure", end="\n")
    if os.getenv("CI"):
        print("-" * LINE_LENGTH)
        print(result.stdout.decode("utf8"))
        print("-" * LINE_LENGTH)
    else:
        print(f" ↳ to get more info, run: {' '.join(command)}", end="\n\n")
    return 1


def run(*args) -> int:
    """run a simple bash command"""
    return subprocess.run(args, capture_output=False, check=False).returncode
