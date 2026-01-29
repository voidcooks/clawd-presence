#!/usr/bin/env python3
"""
Clawd Presence Display
Terminal-based status display for AI agents.
"""

import curses
import json
import time
import math
import os
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent
CONFIG_FILE = SCRIPT_DIR.parent / "config.json"
STATE_FILE = SCRIPT_DIR.parent / "state.json"


def load_config():
    """Load display configuration."""
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


def load_state():
    """Load current agent state."""
    default = {"state": "idle", "message": "", "updated": time.time()}
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE) as f:
                default.update(json.load(f))
        except (json.JSONDecodeError, IOError):
            pass
    return default


def save_state(state_data):
    """Save state to file."""
    with open(STATE_FILE, "w") as f:
        json.dump(state_data, f)


def get_file_mtime(filepath):
    """Get file modification time, or 0 if doesn't exist."""
    try:
        return filepath.stat().st_mtime
    except (OSError, IOError):
        return 0


def load_monogram(letter):
    """Load monogram design for a letter."""
    mono_file = SCRIPT_DIR.parent / "assets" / "monograms" / f"{letter.upper()}.txt"
    if mono_file.exists():
        with open(mono_file) as f:
            return [line.rstrip() for line in f.readlines()]
    # Fallback: simple block letter
    return [
        f"  {letter.upper()}  ",
        f" {letter.upper()}{letter.upper()}{letter.upper()} ",
        f"{letter.upper()}   {letter.upper()}",
        f"{letter.upper()}{letter.upper()}{letter.upper()}{letter.upper()}{letter.upper()}",
        f"{letter.upper()}   {letter.upper()}",
    ]


def build_pulse(pos, width, state):
    """Pre-compute pulse string."""
    if state == "sleep":
        return "─" * width
    
    chars = []
    for i in range(width):
        dist = min(abs(i - pos), width - abs(i - pos))
        if dist == 0:
            chars.append("█")
        elif dist == 1:
            chars.append("▓")
        elif dist == 2:
            chars.append("▒")
        elif dist == 3:
            chars.append("░")
        else:
            chars.append("─")
    return "".join(chars)


def draw(stdscr):
    """Main display loop."""
    curses.start_color()
    curses.use_default_colors()

    # Color palette - grayscale
    curses.init_pair(1, 255, -1)  # Bright white
    curses.init_pair(2, 252, -1)  # White
    curses.init_pair(3, 248, -1)  # Light gray
    curses.init_pair(4, 244, -1)  # Mid gray
    curses.init_pair(5, 240, -1)  # Dark gray
    curses.init_pair(6, 236, -1)  # Darker gray

    # State accent colors
    curses.init_pair(10, 73, -1)   # Dusty cyan (idle)
    curses.init_pair(11, 108, -1)  # Sage green (work)
    curses.init_pair(12, 179, -1)  # Warm gold (think)
    curses.init_pair(13, 167, -1)  # Muted red (alert)
    curses.init_pair(14, 67, -1)   # Steel blue (sleep)

    state_colors = {"idle": 10, "work": 11, "think": 12, "alert": 13, "sleep": 14}
    pulse_speeds = {"idle": 0.08, "work": 0.15, "think": 0.12, "alert": 0.15, "sleep": 0}
    glow_speeds = {"idle": 0.03, "work": 0.06, "think": 0.04, "alert": 0.08, "sleep": 0}

    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(33)  # ~30fps

    # Initial load
    config = load_config()
    state_data = load_state()
    monogram = load_monogram(config["letter"])
    
    # Tracking
    frame = 0
    state_mtime = get_file_mtime(STATE_FILE)
    config_mtime = get_file_mtime(CONFIG_FILE)
    last_state = None
    last_message = None
    last_time_str = ""
    
    # Pulse width
    pulse_width = 32

    stdscr.clear()

    while True:
        try:
            key = stdscr.getch()
            if key in (ord("q"), ord("Q"), 27):  # q, Q, or ESC
                break

            now = time.time()
            
            # Check state file by mtime (fast)
            new_state_mtime = get_file_mtime(STATE_FILE)
            if new_state_mtime != state_mtime:
                state_data = load_state()
                state_mtime = new_state_mtime
                
                # Auto-idle timeout check
                if config["idle_timeout"] > 0:
                    elapsed = now - state_data.get("updated", now)
                    if elapsed > config["idle_timeout"] and state_data["state"] not in ("idle", "sleep"):
                        state_data["state"] = "idle"
                        state_data["message"] = ""
                        save_state(state_data)
            
            # Check config file by mtime (fast)
            new_config_mtime = get_file_mtime(CONFIG_FILE)
            if new_config_mtime != config_mtime:
                new_config = load_config()
                if new_config["letter"] != config["letter"]:
                    monogram = load_monogram(new_config["letter"])
                config = new_config
                config_mtime = new_config_mtime

            state = state_data.get("state", "idle")
            message = state_data.get("message", "")

            # Auto-sleep during configured hours
            hour = datetime.now().hour
            if (hour >= config["sleep_start"] or hour < config["sleep_end"]) and state == "idle":
                state = "sleep"

            h, w = stdscr.getmaxyx()
            cx, cy = w // 2, h // 2
            accent = state_colors.get(state, 10)

            # === MONOGRAM ===
            mark_y = cy - len(monogram) // 2 - 3
            glow_speed = glow_speeds.get(state, 0.03)
            
            if state == "sleep":
                brightness = 4  # Dim
            else:
                glow = (math.sin(frame * glow_speed) + 1) / 2
                brightness = 2 if glow > 0.5 else 3

            for i, line in enumerate(monogram):
                x = cx - len(line) // 2
                y = mark_y + i
                if 0 <= y < h - 1 and 0 <= x < w - 1:
                    try:
                        stdscr.attron(curses.color_pair(brightness))
                        stdscr.addstr(y, x, line[: w - x - 1])
                        stdscr.attroff(curses.color_pair(brightness))
                    except curses.error:
                        pass

            # === PULSE LINE ===
            pulse_y = mark_y + len(monogram) + 1
            pulse_x = cx - pulse_width // 2
            
            if 0 <= pulse_y < h - 1 and pulse_x >= 0:
                speed = pulse_speeds.get(state, 0.08)
                pos = int((frame * speed) % pulse_width) if speed > 0 else 0
                pulse = build_pulse(pos, pulse_width, state)
                
                color = 6 if state == "sleep" else accent
                try:
                    stdscr.attron(curses.color_pair(color))
                    stdscr.addstr(pulse_y, pulse_x, pulse)
                    stdscr.attroff(curses.color_pair(color))
                except curses.error:
                    pass

            # === STATE (only redraw on change) ===
            status_y = pulse_y + 3
            if state != last_state and 0 <= status_y < h - 1:
                state_str = state.upper()
                try:
                    stdscr.addstr(status_y, cx - 10, " " * 20)
                    stdscr.attron(curses.color_pair(accent))
                    stdscr.addstr(status_y, cx - len(state_str) // 2, state_str)
                    stdscr.attroff(curses.color_pair(accent))
                except curses.error:
                    pass
                last_state = state

            # === MESSAGE (only redraw on change) ===
            msg_y = pulse_y + 5
            if message != last_message and 0 <= msg_y < h - 1:
                try:
                    stdscr.addstr(msg_y, 2, " " * (w - 4))
                    if message:
                        msg = message[: w - 4]
                        stdscr.attron(curses.color_pair(5))
                        stdscr.addstr(msg_y, cx - len(msg) // 2, msg)
                        stdscr.attroff(curses.color_pair(5))
                except curses.error:
                    pass
                last_message = message

            # === CORNERS ===
            try:
                stdscr.attron(curses.color_pair(6))
                stdscr.addch(0, 0, "+")
                stdscr.addch(0, w - 2, "+")
                stdscr.addch(h - 2, 0, "+")
                stdscr.addch(h - 2, w - 2, "+")
                stdscr.attroff(curses.color_pair(6))
            except curses.error:
                pass

            # === TIME (only redraw on change) ===
            time_str = datetime.now().strftime("%H:%M")
            if time_str != last_time_str:
                try:
                    stdscr.attron(curses.color_pair(6))
                    stdscr.addstr(1, cx - len(time_str) // 2, time_str)
                    stdscr.attroff(curses.color_pair(6))
                except curses.error:
                    pass
                last_time_str = time_str

            # === NAME ===
            name = config.get("name", "AGENT")
            try:
                stdscr.attron(curses.color_pair(6))
                stdscr.addstr(h - 2, cx - len(name) // 2, name)
                stdscr.attroff(curses.color_pair(6))
            except curses.error:
                pass

            stdscr.refresh()
            frame += 1

        except curses.error:
            pass
        except KeyboardInterrupt:
            break


def main():
    """Entry point."""
    if not STATE_FILE.exists():
        save_state({"state": "idle", "message": "", "updated": time.time()})
    curses.wrapper(draw)


if __name__ == "__main__":
    main()
