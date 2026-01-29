# Clawd Presence

Physical presence display for AI agents. Shows what your agent is doing in real-time.

Most people run their agents headless. This gives them a face.

![States](https://img.shields.io/badge/states-idle%20%7C%20work%20%7C%20think%20%7C%20alert%20%7C%20sleep-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-blue)

## Why?

Chat interfaces have latency. You message your agent, wait, wonder if it's stuck. A presence display inverts this - the agent broadcasts its state continuously.

- **Faster feedback** - Glance at the screen, know what's happening
- **No interruption** - Don't have to ask "what are you doing?"
- **Accountability** - Agent can't silently stall

## Quick Start

```bash
# Clone
git clone https://github.com/voidcooks/clawd-presence.git
cd clawd-presence

# Configure your letter
python3 scripts/configure.py --letter A --name "AGENT"

# Run display (in a dedicated terminal/screen)
python3 scripts/display.py

# Update status from your agent
python3 scripts/status.py work "Building something"
```

## States

| State | Color | When to use |
|-------|-------|-------------|
| `idle` | Cyan | Ready, waiting |
| `work` | Green | Actively doing something |
| `think` | Yellow | Processing, analyzing |
| `alert` | Red | Needs human attention |
| `sleep` | Blue | Inactive hours |

## Auto-Detection

If you're running Clawdbot, auto-detect your agent's name:

```bash
python3 scripts/configure.py --auto
```

## Configuration

```bash
# Set letter and name
python3 scripts/configure.py --letter E --name "EMMA"

# Set auto-idle timeout (default 5 min)
python3 scripts/configure.py --timeout 300

# Set sleep hours (default 11pm-7am)
python3 scripts/configure.py --sleep-start 23 --sleep-end 7

# View current config
python3 scripts/configure.py --show
```

## Custom Monograms

Letter designs are in `assets/monograms/`. Edit or replace with your own.

Regenerate all:
```bash
python3 scripts/generate_monograms.py
```

## Integration

Add to your agent's system prompt:

```
Update presence display when starting tasks:
python3 /path/to/clawd-presence/scripts/status.py <state> "<message>"

States: idle, work, think, alert, sleep
```

## Requirements

- Python 3.8+
- Terminal with 256-color support
- `curses` (included in Python on Linux/macOS)

Optional: `pyyaml` for `--auto` detection

## License

MIT
