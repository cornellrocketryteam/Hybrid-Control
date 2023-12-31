"""
controller.py: Manages user commands and actions
"""

from test_stand import TestStand
from view import TUI
from util import *
from labjack import ljm
import time


class Controller:

    def __init__(self, handle: int) -> None:
        self.handle = handle

        ljm.eWriteName(self.handle, "STREAM_TRIGGER_INDEX", 0)
        ljm.eWriteName(self.handle, "STREAM_CLOCK_SOURCE", 0)
        ljm.eWriteName(self.handle, "STREAM_SETTLING_US", 1000)
        ljm.eWriteName(self.handle, "STREAM_RESOLUTION_INDEX", 4)
        ljm.eWriteName(self.handle, "AIN_ALL_NEGATIVE_CH", 199)
        ljm.eWriteName(self.handle, "AIN_ALL_RANGE", 10.0)
        ljm.eWriteName(self.handle, "DAC1", 5)
              
        self.last_command = ""
        self.test_stand = TestStand(handle)
        self.tui = TUI(self.test_stand)
       

        info = ljm.getHandleInfo(self.handle)

        self.awaiting_mode = -1

        self.ain_data = []
        #Setting sensor ranges, negative channels
        aNames = ["AIN60_NEGATIVE_CH", "AIN60_RANGE",
                "AIN48_NEGATIVE_CH", "AIN48_RANGE",
                "AIN49_NEGATIVE_CH", "AIN49_RANGE",
                "AIN0_RANGE", "AIN1_RANGE", "AIN2_RANGE", "AIN60_RANGE"]
        aValues = [ljm.constants.GND, 2.4,
                56, 0.1,
                57, 0.1,
                10.0, 10.0, 10.0, 10.0]
        ljm.eWriteNames(self.handle, len(aNames), aNames, aValues)

    def run(self) -> None:
                    
        while True:
            try:
                self.tui.update_screen(self.ain_data)
                c = self.tui.get_input()

                input_str = self.tui.input_str
                input_str = input_str[2:]
                
                #Process up arrow to replace text box with last command
                if c == KEY_UPARROW: 
                    self.tui.input_str = "> " + self.last_command

                #Handle Valve Buttons
                if input_str == "" and c in [KEYPAD_0,KEYPAD_1,KEYPAD_2,KEYPAD_3,KEYPAD_DOT,KEYPAD_DASH]: #Valve keypad
                    if c == KEYPAD_0:
                        self.tui.input_str = "> sv 1 " + state_onoff(self.test_stand.sv_states[0])
                    elif c == KEYPAD_1:
                        self.tui.input_str = "> sv 2 " + state_onoff(self.test_stand.sv_states[1])
                    elif c == KEYPAD_2:
                        self.tui.input_str = "> sv 3 " + state_onoff(self.test_stand.sv_states[2])
                    elif c == KEYPAD_3:
                        self.tui.input_str = "> sv 4 " + state_onoff(self.test_stand.sv_states[3])
                    elif c == KEYPAD_DOT:
                        self.tui.input_str = "> sv 5 " + state_onoff(self.test_stand.sv_states[4])
                    elif c == KEYPAD_DASH:
                        self.tui.input_str = "> mav 1 " + state_onoff(self.test_stand.mav_states[0])
                    
                #Handle State Buttons
                if input_str == "" and c in KEYPAD_MODE_BUTTONS : #Mode Popups
                    index = KEYPAD_MODE_BUTTONS.index(c)
                    if self.awaiting_mode == index:
                        self.tui.end_await()
                        self.awaiting_mode = -1

                    else:
                        self.tui.await_mode(Mode(index))
                        self.awaiting_mode = index

                    self.tui.clear()
                    continue
                
                #Handle State Confirmations
                if input_str == "" and (c in KEY_ENTER):
                    if self.awaiting_mode != -1:
                        if self.awaiting_mode == 4:
                            self.tui.supercharged = True 
                        self.test_stand.confirm_mode(Mode(self.awaiting_mode))
                        self.tui.to_mode(Mode(self.awaiting_mode))

                        self.tui.clear()
                        continue
                    
                if c == 27:
                    break

                #Handle Enter Key
                elif c in KEY_ENTER:
                    if input_str in valid_commands:
                        self.last_command = input_str
                        if input_str == "quit":
                            break
                        words = input_str.split(" ")

                        if words[0] == "sv":
                            if words[2] == "on":
                                self.test_stand.sv_on(int(words[1]))
                            elif words[2] == "off":
                                self.test_stand.sv_off(int(words[1]))
                        elif words[0] == "mav":
                            if words[2] == "on":
                                self.test_stand.mav_on(int(words[1]))
                            else:
                                self.test_stand.mav_off(int(words[1]))
                    self.tui.input_str = "> "
                    self.tui.clear()
                elif c in KEY_BACKSPACE:
                    if len(input_str) > 0:
                        self.tui.input_str = self.tui.input_str[:-1]
                        self.tui.clear()

                #Handle Letter Inputs
                else:
                    if c not in [-1, KEYPAD_0, KEYPAD_1, KEYPAD_2, KEYPAD_3, KEYPAD_DOT, KEYPAD_DASH, KEY_UPARROW]:
                        self.tui.input_str += chr(c)

            except KeyboardInterrupt:
                self.handle.close()
                print("run fail")
    
    def read(self) -> None:
        """
        Streams data from the analog input channels on the LabJack handle as defined in ain_channels.
        """

        try:
            with open("labjack_data.csv", 'a') as file:

                aScanListNames = ain_channels
                numAddresses = len(aScanListNames)
                aScanList = ljm.namesToAddresses(numAddresses, aScanListNames)[0]
                scanRate = 70
                scansPerRead = int(scanRate / 2)
                scanRate = ljm.eStreamStart(self.handle, scansPerRead, numAddresses, aScanList, scanRate)

                start = time.time()
                totalScans = 0
                totalSamples = 0
                totalSkip = 0  # Total skipped samples [what does this mean]

                while True:

                    ret = ljm.eStreamRead(self.handle)

                    aData = ret[0]

                    if len(aData) % scansPerRead != 0 or len(aData) % numAddresses != 0:
                        raise Exception("Stream Read has an incorrect number of samples: {} {} {}".format(len(aData), scansPerRead, numAddresses))
                    totalScans += len(aData) / numAddresses
                    totalSamples += len(aData)                

                    for j in range(0, len(aData), numAddresses):
                        data_temp = []
                        for k in range(j, j+numAddresses):
                            if aData[k] == -9999.0:
                                totalSkip += 1
                            file.write(str(round(aData[k], 10)) + ", ")
                            data_temp.append(round(aData[k], 10))
                        file.write('\n')
                        self.ain_data = data_temp

                end = time.time()

                ljm.eStreamStop(self.handle)
        except KeyboardInterrupt:
            self.handle.close()
            pass

        except Exception as e:
            print(e)