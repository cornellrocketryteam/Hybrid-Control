"""
controller.py: Manages user commands and actions
"""

from test_stand import TestStand
import view
import curses

stdscr = curses.initscr()
curses.echo()
stdscr.clear()

class Controller:

    def __init__(self) -> None:
        self.test_stand = TestStand()


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
                    stdscr.addstr(i+3, 0, sv_str)

                mav_str = "MAV:  {state}".format(state = "ON" if self.test_stand.mav_state else "OFF")
                stdscr.addstr(3, 30, mav_str)

                srbv_str = "SRBV: {state}".format(state = "ON" if self.test_stand.srbv_state else "OFF")
                stdscr.addstr(4, 30, srbv_str)
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
                        if len(words) == 3:
                            if words[2] == "on":
                                self.test_stand.sv_states[int(words[1]) - 1] = True
                            else:
                                self.test_stand.sv_states[int(words[1]) - 1] = False
                        elif len(words) == 2:
                            if words[1] == "on":
                                for i in range(0, len(self.test_stand.sv_states)):
                                    self.test_stand.sv_states[i] = True
                            else:
                                for i in range(0, len(self.test_stand.sv_states)):
                                    self.test_stand.sv_states[i] = False

                    if words[0] == "mav":
                        if words[1] == "on":
                            self.test_stand.mav_state = True
                        else:
                            self.test_stand.mav_state = False

                    if words[0] == "srbv":
                        if words[1] == "off":
                            self.test_stand.srbv_state = False

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
        
