#!/usr/bin/env python3
"""
Configure agent presence display.

Usage:
    python3 configure.py --auto              # Auto-detect from clawdbot config
    python3 configure.py --letter A
    python3 configure.py --name "ATLAS"
    python3 configure.py --timeout 300
    python3 configure.py --letter C --name "CLAUDE" --timeout 600
"""

import argparse
import json
import os
from pathlib import Path

CONFIG_FILE = Path(__file__).parent.parent / "config.json"

# Common clawdbot config locations
CLAWDBOT_CONFIG_PATHS = [
    Path.home() / ".config" / "clawd" / "config.yaml",
    Path.home() / ".config" / "clawd" / "config.yml",
    Path.home() / ".clawd" / "config.yaml",
    Path.home() / ".clawd" / "config.yml",
]


def get_clawdbot_agent_name():
    """Try to read agent name from clawdbot config."""
    try:
        import yaml
    except ImportError:
        return None
    
    for config_path in CLAWDBOT_CONFIG_PATHS:
        if config_path.exists():
            try:
                with open(config_path) as f:
                    config = yaml.safe_load(f)
                    # Try common config structures
                    if isinstance(config, dict):
                        # Direct agent.name
                        if "agent" in config and isinstance(config["agent"], dict):
                            name = config["agent"].get("name")
                            if name:
                                return name
                        # Top-level name
                        if "name" in config:
                            return config["name"]
            except Exception:
                continue
    return None


def load_config():
    """Load existing config or defaults."""
    default = {
        "letter": "A",
        "name": "AGENT",
        "idle_timeout": 300,
        "sleep_start": 23,
        "sleep_end": 7,
    }
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE) as f:
                default.update(json.load(f))
        except (json.JSONDecodeError, IOError):
            pass
    return default


def save_config(config):
    """Save config to file."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Configure agent presence display")
    parser.add_argument("--auto", "-a", action="store_true", help="Auto-detect from clawdbot config")
    parser.add_argument("--letter", "-l", type=str, help="Monogram letter (A-Z)")
    parser.add_argument("--name", "-n", type=str, help="Display name")
    parser.add_argument("--timeout", "-t", type=int, help="Auto-idle timeout in seconds (0 to disable)")
    parser.add_argument("--sleep-start", type=int, help="Hour to auto-sleep (0-23)")
    parser.add_argument("--sleep-end", type=int, help="Hour to wake from auto-sleep (0-23)")
    parser.add_argument("--show", "-s", action="store_true", help="Show current config")
    
    args = parser.parse_args()
    config = load_config()
    
    if args.show:
        print(json.dumps(config, indent=2))
        return
    
    changed = False
    
    # Auto-detect from clawdbot config
    if args.auto:
        agent_name = get_clawdbot_agent_name()
        if agent_name:
            first_letter = agent_name[0].upper()
            if first_letter.isalpha():
                config["letter"] = first_letter
                config["name"] = agent_name.upper()
                changed = True
                print(f"Auto-detected: {agent_name} -> letter '{first_letter}'")
        else:
            print("Could not auto-detect agent name from clawdbot config")
            print("Install PyYAML (pip install pyyaml) and ensure config exists")
            return
    
    if args.letter:
        letter = args.letter.upper()
        if len(letter) != 1 or not letter.isalpha():
            print("Error: Letter must be a single A-Z character")
            return
        config["letter"] = letter
        changed = True
    
    if args.name:
        config["name"] = args.name.upper()
        changed = True
    
    if args.timeout is not None:
        config["idle_timeout"] = max(0, args.timeout)
        changed = True
    
    if args.sleep_start is not None:
        config["sleep_start"] = args.sleep_start % 24
        changed = True
    
    if args.sleep_end is not None:
        config["sleep_end"] = args.sleep_end % 24
        changed = True
    
    if changed:
        save_config(config)
        print("Configuration updated:")
        print(json.dumps(config, indent=2))
    else:
        print("Current configuration:")
        print(json.dumps(config, indent=2))
        print("\nUse --help to see options")


if __name__ == "__main__":
    main()
