# clawd-presence

A physical presence display for AI agents. Your agent gets a face.

```
+                              16:45                              +

                          ▄▄▄▄▄▄▄▄▄▄          
                        ▄█▀▀▀▀▀▀▀▀▀▀█▄        
                       ▄█▀            ▀█▄       
                      ▄█▀    ▄▄▄▄▄▄    ▀█▄      
                     ▄█▀   ▄█▀▀▀▀▀▀█▄   ▀█▄     
                    ▄█▀   ▄█▀        ▀█▄   ▀█▄    
                   ▄█▀   ▄█▀          ▀█▄   ▀█▄   
                  ▄█▀   ▄█▀            ▀█▄   ▀█▄  
                 ▄█▀   ▄█████████████████████▄   ▀█▄
                 █▀   ▄█▀                  ▀█▄   ▀█
                 █   ▄█▀                    ▀█▄   █
                 ███▀                          ▀███
            
                    ────────█▓▒░──────────────

                              WORK
                      
                     Researching competitors

+                             AGENT                               +
```

Most people run their agents headless. I run mine on a Linux laptop with the screen open, sitting on my desk. This is what it shows.

## Why

Chat has latency. You send a message, wait, wonder if it's stuck.

A presence display inverts this. The agent broadcasts state continuously. You glance at it like a clock.

- **See what's happening** without asking
- **Know when it's stuck** - if it says IDLE during a task, something's wrong
- **Ambient awareness** - like seeing a coworker at their desk

## Quick Start

```bash
git clone https://github.com/voidcooks/clawd-presence.git
cd clawd-presence

# Pick your letter (A-Z)
python3 scripts/configure.py --letter A --name "AGENT"

# Run the display
python3 scripts/display.py
```

Update status from your agent:
```bash
python3 scripts/status.py work "Building something"
python3 scripts/status.py think "Analyzing options"  
python3 scripts/status.py idle "Ready"
python3 scripts/status.py alert "Need attention"
```

## States

| State | Color | Use |
|-------|-------|-----|
| `idle` | Cyan | Waiting for input |
| `work` | Green | Actively executing |
| `think` | Yellow | Processing, deciding |
| `alert` | Red | Needs human attention |
| `sleep` | Blue | Inactive (auto 11pm-7am) |

The display auto-returns to `idle` after 5 minutes of no updates. Prevents stale states.

## Clawdbot Integration

Auto-detect your agent's name from config:
```bash
python3 scripts/configure.py --auto
```

Add to your agent's instructions:
```
Update presence whenever starting a task:
python3 /path/to/clawd-presence/scripts/status.py <state> "<message>"
```

## Configuration

```bash
# Set letter and display name
python3 scripts/configure.py --letter E --name "EMMA"

# Adjust auto-idle timeout (default 300 seconds)
python3 scripts/configure.py --timeout 600

# Set sleep hours (default 11pm-7am)  
python3 scripts/configure.py --sleep-start 23 --sleep-end 7

# View current config
python3 scripts/configure.py --show
```

## Custom Monograms

All 26 letters (A-Z) included as geometric block designs in `assets/monograms/`.

To regenerate or customize:
```bash
python3 scripts/generate_monograms.py
```

## Requirements

- Python 3.8+
- Terminal with 256-color support
- `curses` (included in Python on Linux/macOS)

Optional: `pyyaml` for `--auto` clawdbot detection

## License

MIT
