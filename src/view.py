"""
view.py: Manages the text-based user interface
"""

import curses
from util import Mode, sensor_keys

class TUI:
    def __init__(self, test_stand) -> None:
        self.stdscr = curses.initscr()
        self.stdscr.nodelay(True)
        curses.echo()
        curses.start_color()
        curses.use_default_colors()
        self.stdscr.clear()

        self.input_str = "> "

        self.test_stand = test_stand

        self.awaited_mode = -1

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
    
    def update_screen(self, ain_data): #, data_list: list) -> None:

        with open("test_shared.csv", 'a') as file:
            data_dict = self.convert_data(ain_data, self.test_stand.sensor_dict)
            file.write(str(data_dict))
            file.write("\n") 

        
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

        if self.awaited_mode != -1:
            self.stdscr.addstr(curses.LINES - 3, 0, "Confirm")
            self.stdscr.addstr(curses.LINES - 3, 8, self.modes[self.awaited_mode], curses.A_BOLD)
        else:
            self.stdscr.addstr(curses.LINES - 3, 0, "")
        self.stdscr.addstr(curses.LINES - 1, 0, self.input_str)

    def get_input(self) -> int:
        c = self.stdscr.getch()
        return c
    
    def await_mode(self, mode: Mode) -> None:
        self.awaited_mode = mode.value

    def end_await(self) -> None:
        self.awaited_mode = -1

    def to_mode(self, mode: Mode) -> None:
        self.awaited_mode = -1
        self.mode = mode.value
    
    def clear(self) -> None:
        self.stdscr.clear()
    
    def convert_data(self, data_list: list, sensor_dict: dict) -> dict:
        """
        Takes a list of data values and returns a dictionary
        with the sensor name as a key and its corresponding
        scaled data as a value.
        """
        data_dict = {}
        for i in range(len(data_list)):
            s = sensor_dict[i]
            data_dict[sensor_keys[i]] = (-1) * s.scale(data_list[i])
        return data_dict