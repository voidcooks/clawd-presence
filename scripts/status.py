#!/usr/bin/env python3
"""
Update agent presence status.

Usage:
    python3 status.py work "Building feature X"
    python3 status.py idle
    python3 status.py think "Analyzing options"
    python3 status.py alert "Need human input"
    python3 status.py sleep
"""

import json
import sys
import time
from pathlib import Path

STATE_FILE = Path(__file__).parent.parent / "state.json"

VALID_STATES = {"idle", "work", "think", "alert", "sleep"}


def update_status(state: str, message: str = ""):
    """Update the presence state file."""
    state = state.lower()
    
    if state not in VALID_STATES:
        print(f"Invalid state: {state}")
        print(f"Valid states: {', '.join(sorted(VALID_STATES))}")
        sys.exit(1)
    
    data = {
        "state": state,
        "message": message,
        "updated": time.time(),
    }
    
    with open(STATE_FILE, "w") as f:
        json.dump(data, f, indent=2)
    
    if message:
        print(f"{state.upper()}: {message}")
    else:
        print(state.upper())


def main():
    if len(sys.argv) < 2:
        print("Usage: status.py <state> [message]")
        print(f"States: {', '.join(sorted(VALID_STATES))}")
        sys.exit(1)
    
    state = sys.argv[1]
    message = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
    
    update_status(state, message)


if __name__ == "__main__":
    main()
