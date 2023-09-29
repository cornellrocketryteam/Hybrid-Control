"""
controller.py: Manages user commands and actions
"""

from test_stand import TestStand
import view
import curses

stdscr = curses.initscr()
curses.echo()
#curses.start_color()
stdscr.clear()

class Controller:

    def __init__(self, handle: int) -> None:
        self.test_stand = TestStand(handle)
        self.handle = handle

    def run(self) -> None:
        input_str = "> "
        try:
            while True:
                stdscr.refresh()

                # Display

                stdscr.addstr(0, 0, "=" * curses.COLS)
                stdscr.addstr(1, 0, "Hybrid Test Stand Control")
                stdscr.addstr(2, 0, "=" * curses.COLS)

                for i in range(0, len(self.test_stand.sv_states)):
                    sv_str = "SV {num}: {state}".format(num = i+1, state = "ON" if self.test_stand.sv_states[i] else "OFF")
                    stdscr.addstr(i+4, 0, sv_str)

                mav_str_1 = "MAV 1: {state}".format(state = "ON" if self.test_stand.mav_states[0] else "OFF")
                mav_str_2 = "MAV 2: {state}".format(state = "ON" if self.test_stand.mav_states[1] else "OFF")
                stdscr.addstr(10, 0, mav_str_1)
                stdscr.addstr(11, 0, mav_str_2)

                stdscr.addstr(4, 50, "Default")

                stdscr.addstr(6, 50, "Prefire purge tanks")
                stdscr.addstr(7, 50, "Prefire purge engine")
                stdscr.addstr(8, 50, "Fill")
                stdscr.addstr(9, 50, "Supercharge")
                stdscr.addstr(10, 50, "Ignition")
                stdscr.addstr(11, 50, "Fire")

                stdscr.addstr(curses.LINES - 1, 0, input_str)

                # Process input

                c = stdscr.getch()

                if c == 27:
                    break
                elif c == curses.KEY_ENTER or c == 10 or c == 13:

                    input_str = input_str[2:]

                    if input_str == "quit":
                        break

                    words = input_str.split(" ")

                    if words[0] == "sv":
                        if words[2] == "on":
                            self.test_stand.sv_on(int(words[1]))
                        else:
                            self.test_stand.sv_off(int(words[1]))

                    if words[0] == "mav":
                        if words[2] == "on":
                            self.test_stand.mav_on(int(words[1]))
                        else:
                            self.test_stand.mav_off(int(words[1]))

                    input_str = "> "
                    stdscr.clear()

                elif c == curses.KEY_BACKSPACE or c == 127:
                    if len(input_str) > 2:
                        input_str = input_str[:-1]
                        stdscr.clear()
                else:
                    input_str += chr(c)

        except KeyboardInterrupt:
            # Teardown
            pass
        