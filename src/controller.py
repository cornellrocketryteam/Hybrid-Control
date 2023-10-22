"""
controller.py: Manages user commands and actions
"""

from test_stand import TestStand
from view import TUI
import curses
from util import Mode

class Controller:

    def __init__(self, handle: int) -> None:
        self.test_stand = TestStand(handle)
        self.tui = TUI(self.test_stand)
        self.handle = handle

        self.awaiting_mode = -1

        self.awaiting_mappings = [52, 53, 54, 43, 55, 56, 57]

    def run(self) -> None:
        try:
            while True:
                self.tui.update_screen()
                c = self.tui.get_input()

                input_str = self.tui.input_str
                input_str = input_str[2:]

                if input_str == "" and ((c >= 52 and c <= 61) or c == 43):
                    index = self.awaiting_mappings.index(c)

                    if self.awaiting_mode == index:
                        self.tui.end_await()
                        self.awaiting_mode = -1

                    else:
                        self.tui.await_mode(Mode(index))
                        self.awaiting_mode = index

                    self.tui.clear()
                    continue

                if input_str == "" and (c == curses.KEY_ENTER or c == 10 or c == 13):
                    if self.awaiting_mode != -1:
                        self.test_stand.confirm_mode(Mode(self.awaiting_mode))
                        self.tui.to_mode(Mode(self.awaiting_mode))

                        self.tui.clear()
                        continue
                    
                if c == 27:
                    break
                elif c == curses.KEY_ENTER or c == 10 or c == 13:

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

                    self.tui.input_str = "> "
                    self.tui.clear()

                elif c == curses.KEY_BACKSPACE or c == 127:
                    if len(input_str) > 2:
                        self.tui.input_str = self.tui.input_str[:-1]
                        self.tui.clear()
                else:
                    self.tui.input_str += chr(c)

        except KeyboardInterrupt:
            pass