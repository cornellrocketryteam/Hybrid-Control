"""
view.py: Manages the text-based user interface
"""

import curses
from util import Mode

class TUI:
    def __init__(self, test_stand) -> None:
        self.stdscr = curses.initscr()
        curses.echo()
        #curses.start_color()
        self.stdscr.clear()

        self.input_str = "> "

        self.test_stand = test_stand

        self.modes = [
            "Default", 
            "Prefire purge tanks", 
            "Prefire purge engine",
            "Fill",
            "Supercharge",
            "Ignition",
            "Fire"
        ]
        
        self.mode = 0
        self.supercharged = False
    
    def update_screen(self) -> None:
        self.stdscr.refresh()

        self.stdscr.addstr(0, 0, "=" * curses.COLS)
        self.stdscr.addstr(1, 0, "Hybrid Test Stand Control", curses.A_BOLD)
        self.stdscr.addstr(2, 0, "=" * curses.COLS)

        for i in range(0, len(self.test_stand.sv_states)):
            sv_str = "SV {num}: {state}".format(num = i+1, state = "ON" if self.test_stand.sv_states[i] else "OFF")
            self.stdscr.addstr(i+4, 0, sv_str)

        mav_str_1 = "MAV 1: {state}".format(state = "ON" if self.test_stand.mav_states[0] else "OFF")
        mav_str_2 = "MAV 2: {state}".format(state = "ON" if self.test_stand.mav_states[1] else "OFF")
        self.stdscr.addstr(10, 0, mav_str_1)
        self.stdscr.addstr(11, 0, mav_str_2)

        if self.mode == 0:
            self.stdscr.addstr(4, 48, "* " + self.modes[0], curses.A_BOLD)
        else:
            self.stdscr.addstr(4, 50, self.modes[0])

        for i in range(1, 7):
            if i == 4:
                if self.supercharged:
                    self.stdscr.addstr(i+5, 50, "Supercharged", curses.A_ITALIC)
                else:
                    self.stdscr.addstr(i+5, 50, self.modes[i])
            else:
                if self.mode == i:
                    self.stdscr.addstr(i+5, 48, "* " + self.modes[i], curses.A_BOLD)
                else:
                    self.stdscr.addstr(i+5, 50, self.modes[i])

        self.stdscr.addstr(curses.LINES - 1, 0, self.input_str)

    def get_input(self) -> int:
        c = self.stdscr.getch()
        return c
    
    def to_mode(self, mode: Mode) -> None:
        self.mode = mode.value
    
    def clear(self) -> None:
        self.stdscr.clear()