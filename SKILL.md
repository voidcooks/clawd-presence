---
name: clawd-presence
description: Physical presence display for AI agents running on a dedicated screen or terminal. Shows a customizable monogram (A-Z), status state, and current activity. Use when setting up an always-on visual indicator of agent activity, or when needing a faster feedback loop than chat for understanding what the agent is doing.
---

# Clawd Presence

Terminal-based presence display for AI agents. Run on a dedicated screen (old laptop, Raspberry Pi, spare monitor) as a physical indicator of what your agent is doing.

## Why This Exists

Chat has latency. You send a message, wait, wonder if it's working. A presence display inverts this: the agent broadcasts state continuously, you glance at it like a clock.

**Faster feedback loop:** See what the agent is doing without asking. "WORK - Researching competitors" tells you more than a spinning cursor.

**Ambient awareness:** Like seeing a coworker at their desk. You know they're there, busy, no need to interrupt.

**Accountability:** Agent can't silently stall. If it says "IDLE" for 10 minutes during a task, something's wrong.

## Setup

```bash
# 1. Copy to your workspace
cp -r clawd-presence ~/workspace/presence
cd ~/workspace/presence

# 2. Configure (auto-detect from clawdbot or set manually)
python3 scripts/configure.py --auto
# or
python3 scripts/configure.py --letter A --name "AGENT"

# 3. Run display
python3 scripts/display.py
```

## Update Status

```bash
python3 scripts/status.py work "Building feature"
python3 scripts/status.py think "Analyzing options"
python3 scripts/status.py idle "Ready"
python3 scripts/status.py alert "Need attention"
python3 scripts/status.py sleep
```

## States

| State | Color | Use |
|-------|-------|-----|
| `idle` | Cyan | Waiting for input |
| `work` | Green | Executing task |
| `think` | Yellow | Processing, deciding |
| `alert` | Red | Needs human |
| `sleep` | Blue | Inactive (auto 11pm-7am) |

## Auto-Idle

Display returns to idle after 5 minutes of no updates. Prevents stale states.

```bash
python3 scripts/configure.py --timeout 300  # seconds, 0 to disable
```

## Agent Integration

Add to agent instructions:
```
Update presence: python3 ~/workspace/presence/scripts/status.py <state> "<message>"
```

## Files

- `scripts/display.py` - Main display
- `scripts/status.py` - Update status
- `scripts/configure.py` - Configure settings
- `assets/monograms/` - Letter designs A-Z
