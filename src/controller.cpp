#include "controller.hpp"
#include "LJMStreamUtil.hpp"
#include "LJMUtil.hpp"
#include "config.hpp"
#include "test_stand.hpp"
#include <LabJackM.h>
#include <fstream>
#include <iostream>
#include <numeric>
#include <signal.h>
#include <sstream>
#include <stdio.h>
#include <string>
#include <vector>

#include <chrono>
#include <ctime>
#include <iomanip>

Controller::Controller(int handle) : test_stand(TestStand(handle)), tui(TUI(&test_stand)), handle(handle) {
    INIT_SCAN_RATE = 70;
    SCANS_PER_READ = (int)INIT_SCAN_RATE / 2;
    aDataSize = NUM_CHANNELS * SCANS_PER_READ;
    aData = new double[sizeof(double) * aDataSize];
    valid_input = false;
    input = "";
}

// Instruct the view to update and process any input commands
void Controller::run(bool &running) {
    while (running) {
        tui.update(aData);

        if (tui.get_command()) {
            if (tui.input.size() > 1) {
                parse_typed_command();
            } else {
                parse_mode_command();
            }

            // TODO: Rework this so controller doesn't have to call clear - Probably pass the command as a buffer from get_command()
            tui.clear_input();
        }
    }
}

bool interrupted = false;

void signalHandler(int signum) {
    interrupted = true;
}

void Controller::read(bool &running) {

    const char *CHANNEL_NAMES[] = {"AIN127", "AIN126", "AIN125", "AIN124", "AIN123", "AIN122", "AIN121", "AIN120",
                                   "AIN3", "AIN1", "AIN2",
                                   "AIN60",
                                   "AIN48", "AIN49"};

    enum { NUM_FRAMES = 10 };
    const char *aNames[] = {"STREAM_TRIGGER_INDEX", "STREAM_CLOCK_SOURCE", "STREAM_RESOLUTION_INDEX",
                            "STREAM_SETTLING_US", "AIN_ALL_RANGE", "AIN_ALL_NEGATIVE_CH",
                            "AIN48_RANGE", "AIN49_RANGE", "AIN48_NEGATIVE_CH", "AIN49_NEGATIVE_CH"};
    const double aValues[] = {0,
                              0,
                              4,
                              1000,
                              10,
                              LJM_GND,
                              0.1, 0.1, 56, 57};

    int err, channel;
    int deviceScanBacklog = 0;
    int LJMScanBacklog = 0;
    unsigned int receiveBufferBytesSize = 0;
    unsigned int receiveBufferBytesBacklog = 0;
    int connectionType;

    int *aScanList = new int[NUM_CHANNELS];

    try {

        WriteNamesOrDie(handle, NUM_FRAMES, aNames, aValues);

        std::ofstream file;
        auto startTime = std::chrono::steady_clock::now();
        file.open("test_data.csv", std::ios::out | std::ios::app);

        err = LJM_GetHandleInfo(handle, NULL, &connectionType, NULL, NULL, NULL, NULL);
        ErrorCheck(err, "LJM_GetHandleInfo");
        memset(aData, 0, sizeof(double) * aDataSize);

        err = LJM_NamesToAddresses(NUM_CHANNELS, CHANNEL_NAMES, aScanList, NULL);
        ErrorCheck(err, "Getting positive channel addresses");

        err = LJM_eStreamStart(handle, SCANS_PER_READ, NUM_CHANNELS, aScanList,
                               &INIT_SCAN_RATE);
        ErrorCheck(err, "LJM_eStreamStart");

        signal(SIGINT, signalHandler);

        while (running) {
            err = LJM_eStreamRead(handle, aData, &deviceScanBacklog,
                                  &LJMScanBacklog);
            ErrorCheck(err, "LJM_eStreamRead");

            if (connectionType != LJM_ctANY) {
                err = LJM_GetStreamTCPReceiveBufferStatus(handle,
                                                          &receiveBufferBytesSize, &receiveBufferBytesBacklog);
                ErrorCheck(err, "LJM_GetStreamTCPReceiveBufferStatus");
            }

            auto currentTime = std::chrono::steady_clock::now() - startTime;
            auto millis = std::chrono::duration_cast<std::chrono::milliseconds>(currentTime).count();

            if (valid_input) {
                file << millis << ", " << input << "\n";
            }

            currentTime = std::chrono::steady_clock::now() - startTime;
            millis = std::chrono::duration_cast<std::chrono::milliseconds>(currentTime).count();
            file << millis << ", ";

            for (channel = 0; channel < NUM_CHANNELS; channel++) {
                file << aData[channel] << ", ";
                file.flush();
            }

            // add clean interval thing? (https://github.com/labjack/C_CPP_LJM/blob/develop/more/ain/dual_ain_loop.c)

            file << "\n";
            valid_input = false;

            running = !interrupted;
        }
        file << "\n";
        file.close();

        err = LJM_eStreamStop(handle);
        ErrorCheck(err, "Stopping stream");

        delete[] aData;
        delete[] aScanList;

    } catch (...) {
        running = false;
    }
}

void Controller::parse_typed_command() {
    if (test_stand.is_awaiting_mode) {
        test_stand.is_awaiting_mode = false;
    }

    // Split up input string by spaces
    std::istringstream iss(tui.input);
    std::vector<std::string> tokens;

    do {
        std::string word;
        iss >> word;
        tokens.push_back(word);
    } while (iss);

    tokens.pop_back();

    for (const auto &str : tokens) {
        input = std::accumulate(
            tokens.begin(), tokens.end(), std::string(),
            [](const std::string &a, const std::string &b) {
                return a + " " + b;
            });
    }

    if (tokens[0] == "sv") {
        if (tokens[1].size() != 1) {
            return;
        }
        int sv = tokens[1].at(0) - '0';
        if (sv < 1 || sv > 5) {
            tui.display_input_error("Invalid SV index \"" + std::to_string(sv) + "\"");
            return;
        }

        if (tokens[2] == "on") {
            test_stand.sv_on(sv);
            valid_input = true;
        } else if (tokens[2] == "off") {
            test_stand.sv_off(sv);
            valid_input = true;
        } else {
            tui.display_input_error("Unknown SV operation \"" + tokens[2] + "\"");
        }
    } else if (tui.input == "mav on") {
        test_stand.mav_on();
        valid_input = true;
    } else if (tui.input == "mav off") {
        test_stand.mav_off();
        valid_input = true;
    } else {
        tui.display_input_error("Unknown command \"" + tui.input + "\"");
        return;
    }
    tui.display_input_error("");
}

void Controller::parse_mode_command() {
    if (tui.input.size() == 0) {
        if (test_stand.is_awaiting_mode) {
            test_stand.to_mode(test_stand.awaited_mode);
            test_stand.is_awaiting_mode = false;
        } else if (test_stand.is_awaiting_valve) {
            if (test_stand.awaited_valve == 5) {
                test_stand.mav_toggle();
            } else {
                test_stand.sv_toggle(test_stand.awaited_valve + 1);
            }
            test_stand.is_awaiting_valve = false;
        }
        tui.display_input_error("");
        return;
    }
    int command = (int)tui.input.at(0);
    input = command;

    for (int i = 0; i < 7; i++) {
        if (command == mode_ascii_mappings[i]) {
            test_stand.is_awaiting_valve = false;
            Mode mode = static_cast<Mode>(i);
            if (test_stand.is_awaiting_mode) {
                if (test_stand.awaited_mode == mode) {
                    test_stand.is_awaiting_mode = false;
                    tui.display_input_error("");
                } else {
                    test_stand.awaited_mode = mode;
                }
            } else {
                test_stand.is_awaiting_mode = true;
                test_stand.awaited_mode = mode;
                tui.display_await_mode();
            }
            valid_input = true;
            return;
        } else if (command == valve_ascii_mappings[i]) {
            test_stand.is_awaiting_mode = false;
            if (test_stand.is_awaiting_valve) {
                if (test_stand.awaited_valve == i) {
                    test_stand.is_awaiting_valve = false;
                    tui.display_input_error("");
                } else {
                    test_stand.awaited_valve = i;
                }
            } else {
                test_stand.is_awaiting_valve = true;
                test_stand.awaited_valve = i;
                tui.display_await_valve();
            }
            valid_input = true;
            return;
        }
    }
    tui.display_input_error("Unknown command \"" + tui.input + "\"");
}