
---

### 🐍 `quick_draw.py`
```python
#!/usr/bin/env python3
"""
🤠 Quick Draw: Terminal Showdown
A Wild West reaction-time duel playable in your terminal.
Press your shoot key only when you see "DRAW!" — too early and you lose!
"""

import curses
import random
import time
import sys

def draw_text(win, y, text, attr=0):
    h, w = win.getmaxyx()
    x = max(0, (w - len(text)) // 2)
    win.addstr(y, x, text, attr)

def duel(stdscr, mode="1P"):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    curses.start_color()
    curses.init_pair(1, curses.COLOR_YELLOW, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    curses.init_pair(3, curses.COLOR_GREEN, -1)
    curses.init_pair(4, curses.COLOR_CYAN, -1)

    draw_text(stdscr, 2, "🤠 QUICK DRAW — TERMINAL SHOWDOWN", curses.A_BOLD | curses.color_pair(1))
    draw_text(stdscr, 4, "Wait for the signal... then SHOOT!")
    draw_text(stdscr, 6, "Press 'F' (Player 1) or 'J' (Player 2) when it says DRAW!")
    draw_text(stdscr, 8, "Press 'Q' anytime to quit.")
    stdscr.refresh()
    time.sleep(3)

    # Pre-round suspense
    wait = random.uniform(2, 6)
    start = time.time()
    too_early = False
    winner = None

    draw_text(stdscr, 10, "...")
    stdscr.refresh()

    while time.time() - start < wait:
        key = stdscr.getch()
        if key in (ord('f'), ord('F')):
            too_early = "Player 1"
            break
        elif key in (ord('j'), ord('J')):
            too_early = "Player 2"
            break
        elif key in (ord('q'), ord('Q')):
            sys.exit(0)
        time.sleep(0.05)

    if too_early:
        stdscr.clear()
        draw_text(stdscr, h//2, f"{too_early} shot too early! 🤦", curses.color_pair(2) | curses.A_BOLD)
        stdscr.refresh()
        time.sleep(2)
        return

    # Signal to DRAW
    stdscr.clear()
    draw_text(stdscr, h//2, "🔥 DRAW! 🔥", curses.color_pair(3) | curses.A_BOLD)
    stdscr.refresh()
    signal_time = time.time()

    reaction_p1 = None
    reaction_p2 = None

    while True:
        key = stdscr.getch()
        if key in (ord('f'), ord('F')):
            reaction_p1 = time.time() - signal_time
            break
        elif key in (ord('j'), ord('J')):
            reaction_p2 = time.time() - signal_time
            break
        elif key in (ord('q'), ord('Q')):
            sys.exit(0)

    # AI mode
    if mode == "1P":
        ai_reaction = random.uniform(0.25, 0.5)
        if reaction_p1 < ai_reaction:
            winner = "Player 1 (You!)"
        else:
            winner = "🤖 AI"
    else:
        if reaction_p1 is not None and reaction_p2 is not None:
            winner = "Tie!"
        elif reaction_p1 is not None:
            winner = "Player 1"
        elif reaction_p2 is not None:
            winner = "Player 2"

    stdscr.clear()
    draw_text(stdscr, h//2 - 1, f"{winner} wins the duel! ⚡", curses.color_pair(4) | curses.A_BOLD)
    draw_text(stdscr, h//2 + 1, "Press any key for another round or 'Q' to quit.")
    stdscr.refresh()

    stdscr.nodelay(False)
    k = stdscr.getch()
    if k in (ord('q'), ord('Q')):
        sys.exit(0)

def menu(stdscr):
    curses.curs_set(0)
    while True:
        stdscr.clear()
        draw_text(stdscr, 2, "🤠 QUICK DRAW — TERMINAL SHOWDOWN", curses.A_BOLD | curses.color_pair(1))
        draw_text(stdscr, 5, "1) Single Player (vs AI)")
        draw_text(stdscr, 6, "2) Two Players (local)")
        draw_text(stdscr, 7, "Q) Quit")
        stdscr.refresh()

        k = stdscr.getch()
        if k == ord('1'):
            duel(stdscr, "1P")
        elif k == ord('2'):
            duel(stdscr, "2P")
        elif k in (ord('q'), ord('Q')):
            break

def run():
    curses.wrapper(menu)

if __name__ == "__main__":
    run()
