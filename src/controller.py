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

    def run(self) -> None:
        try:
            while True:
                self.tui.update_screen()
                c = self.tui.get_input()

                input_str = self.tui.input_str
                input_str = input_str[2:]

                if input_str == "" and ((c >= 52 and c <= 61) or c == 43):
                    if c == 52:
                        self.tui.await_mode(Mode.DEFAULT)
                        self.awaiting_mode = 0
                    if c == 53:
                        self.tui.await_mode(Mode.PREFIRE_PURGE_TANKS)
                        self.awaiting_mode = 1
                    if c == 54:
                        self.tui.await_mode(Mode.PREFIRE_PURGE_ENGINE)
                        self.awaiting_mode = 2
                    if c == 43:
                        self.tui.await_mode(Mode.FILL)
                        self.awaiting_mode = 3
                    if c == 55:
                        self.tui.await_mode(Mode.SUPERCHARGE)
                        self.awaiting_mode = 4
                    if c == 56:
                        self.tui.await_mode(Mode.IGNITION)
                        self.awaiting_mode = 5
                    if c == 57:
                        self.tui.await_mode(Mode.FIRE)
                        self.awaiting_mode = 6

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