"""
controller.py: Manages user commands and actions
"""

from test_stand import TestStand
from view import TUI
import curses
from util import Mode, sensor_keys, ain_channels
from labjack import ljm
import time


class Controller:

    def __init__(self, handle: int) -> None:
        self.test_stand = TestStand(handle)
        self.tui = TUI(self.test_stand)
        self.handle = handle

        self.awaiting_mode = -1

        self.awaiting_mappings = [52, 53, 54, 43, 55, 56, 57]

        self.ain_data = []

        info = ljm.getHandleInfo(self.handle)

        ljm.eWriteName(self.handle, "STREAM_TRIGGER_INDEX", 0)
        ljm.eWriteName(self.handle, "STREAM_CLOCK_SOURCE", 0)
        ljm.eWriteName(self.handle, "STREAM_SETTLING_US", 0)
        ljm.eWriteName(self.handle, "STREAM_RESOLUTION_INDEX", 0)
        ljm.eWriteName(self.handle, "AIN_ALL_NEGATIVE_CH", 199)
        ljm.eWriteName(self.handle, "AIN_ALL_RANGE", 10.0)

        aNames = ["AIN60_NEGATIVE_CH", "AIN60_RANGE",
                "AIN48_NEGATIVE_CH", "AIN48_RANGE",
                "AIN49_NEGATIVE_CH", "AIN49_RANGE",]
        aValues = [ljm.constants.GND, 2.4,
                56, 10.0,
                57, 10.0,]
        ljm.eWriteNames(self.handle, len(aNames), aNames, aValues)

    def run(self) -> None:
                    
        while True:
            try:

                self.tui.update_screen(self.ain_data)
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
                    if c != -1:
                        self.tui.input_str += chr(c)
        #print("after run")

            except KeyboardInterrupt:
                print("run fail")
            #pass
    
    def read(self) -> None:
        """
        Streams data from the analog input channels on the LabJack handle as defined in ain_channels.
        """

        try:
            #print("trying to read")
            with open("labjack_data.csv", 'w') as file:

                aScanListNames = ain_channels
                numAddresses = len(aScanListNames)
                aScanList = ljm.namesToAddresses(numAddresses, aScanListNames)[0]
                scanRate = 100
                scansPerRead = int(scanRate / 2)
                scanRate = ljm.eStreamStart(self.handle, scansPerRead, numAddresses, aScanList, scanRate)

                start = time.time()
                totalScans = 0
                totalSamples = 0
                totalSkip = 0  # Total skipped samples [what does this mean]

                for i in range(0, 10):

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
                            file.write(str(round(aData[k], 3)) + ", ")
                            data_temp.append(round(aData[k], 3))
                        file.write('\n')
                        self.ain_data = data_temp

                end = time.time()

                ljm.eStreamStop(self.handle)
                #print("after read")
        except KeyboardInterrupt:
            pass

        except Exception as e:
            print(e)
        