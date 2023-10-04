"""
view.py: Manages the text-based user interface
"""

import curses


class TUI:
    def __init__(self, test_stand) -> None:
        self.stdscr = curses.initscr()
        curses.echo()
        #curses.start_color()
        self.stdscr.clear()

        self.input_str = "> "

        self.test_stand = test_stand
    
    def update_screen(self) -> None:
        self.stdscr.refresh()

        self.stdscr.addstr(0, 0, "=" * curses.COLS)
        self.stdscr.addstr(1, 0, "Hybrid Test Stand Control")
        self.stdscr.addstr(2, 0, "=" * curses.COLS)

        for i in range(0, len(self.test_stand.sv_states)):
            sv_str = "SV {num}: {state}".format(num = i+1, state = "ON" if self.test_stand.sv_states[i] else "OFF")
            self.stdscr.addstr(i+4, 0, sv_str)

        mav_str_1 = "MAV 1: {state}".format(state = "ON" if self.test_stand.mav_states[0] else "OFF")
        mav_str_2 = "MAV 2: {state}".format(state = "ON" if self.test_stand.mav_states[1] else "OFF")
        self.stdscr.addstr(10, 0, mav_str_1)
        self.stdscr.addstr(11, 0, mav_str_2)

        self.stdscr.addstr(4, 50, "Default")

        self.stdscr.addstr(6, 50, "Prefire purge tanks")
        self.stdscr.addstr(7, 50, "Prefire purge engine")
        self.stdscr.addstr(8, 50, "Fill")
        self.stdscr.addstr(9, 50, "Supercharge")
        self.stdscr.addstr(10, 50, "Ignition")
        self.stdscr.addstr(11, 50, "Fire")

        self.stdscr.addstr(curses.LINES - 1, 0, self.input_str)

    def get_input(self) -> int:
        c = self.stdscr.getch()
        return c
    
    def clear(self) -> None:
        self.stdscr.clear()