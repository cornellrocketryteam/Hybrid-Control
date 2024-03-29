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
        file.open("test_data.csv", std::ios::out | std::ios::app);

        err = LJM_GetHandleInfo(handle, NULL, &connectionType, NULL, NULL, NULL, NULL);
        ErrorCheck(err, "LJM_GetHandleInfo");

        // Clear aData. This is not strictly necessary, but can help debugging.
        memset(aData, 0, sizeof(double) * aDataSize);

        err = LJM_NamesToAddresses(NUM_CHANNELS, CHANNEL_NAMES, aScanList, NULL);
        ErrorCheck(err, "Getting positive channel addresses");

        // printf("\n");
        // printf("Starting stream...\n");
        err = LJM_eStreamStart(handle, SCANS_PER_READ, NUM_CHANNELS, aScanList,
                               &INIT_SCAN_RATE);
        ErrorCheck(err, "LJM_eStreamStart");
        // printf("Stream started. Actual scan rate: %.02f Hz (%.02f sample rate)\n",
        //        INIT_SCAN_RATE, INIT_SCAN_RATE * NUM_CHANNELS);
        // printf("\n");

        signal(SIGINT, signalHandler);

        while (running) {
            err = LJM_eStreamRead(handle, aData, &deviceScanBacklog,
                                  &LJMScanBacklog);
            ErrorCheck(err, "LJM_eStreamRead");

            // printf("iteration: %d - deviceScanBacklog: %d, LJMScanBacklog: %d",
            //        iteration, deviceScanBacklog, LJMScanBacklog);
            if (connectionType != LJM_ctUSB) { // TODO: change for ethernet
                err = LJM_GetStreamTCPReceiveBufferStatus(handle,
                                                          &receiveBufferBytesSize, &receiveBufferBytesBacklog);
                ErrorCheck(err, "LJM_GetStreamTCPReceiveBufferStatus");
                // printf(", receive backlog: %f%%",
                //        ((double)receiveBufferBytesBacklog) / receiveBufferBytesSize * 100);
            }
            // printf("\n");
            // printf("  1st scan out of %d:\n", SCANS_PER_READ);
            auto now = std::chrono::system_clock::now();
            time_t rawtime = std::chrono::system_clock::to_time_t(now);
            std::tm *local_time;
            local_time = localtime(&rawtime);

            if (valid_input) {
                file << std::put_time(local_time, "%F %T") << ", " << input << "\n";
            }

            now = std::chrono::system_clock::now();
            rawtime = std::chrono::system_clock::to_time_t(now);
            local_time = localtime(&rawtime);
            file << std::put_time(local_time, "%F %T") << ", ";

            for (channel = 0; channel < NUM_CHANNELS; channel++) {
                // printf("    %s = %0.5f\n", CHANNEL_NAMES[channel], aData[channel]);
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

        // printf("Stopping stream\n");
        err = LJM_eStreamStop(handle);
        ErrorCheck(err, "Stopping stream");

        delete[] aData;
        delete[] aScanList;

    } catch (...) { // maybe dont put read in try catch? or maybe move ^c catch to main.cpp?
        running = false;
    }
}

void Controller::parse_typed_command() {
    if (test_stand.is_awaiting) {
        test_stand.is_awaiting = false;
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
        if (test_stand.is_awaiting) {
            test_stand.to_mode(test_stand.awaited_mode);
            test_stand.is_awaiting = false;
        }
        tui.display_input_error("");
        return;
    }
    int command = (int)tui.input.at(0);
    input = command;

    for (int i = 0; i < 7; i++) {
        if (command == ascii_mappings[i]) {
            Mode mode = static_cast<Mode>(i);
            if (test_stand.is_awaiting) {
                if (test_stand.awaited_mode == mode) {
                    test_stand.is_awaiting = false;
                    tui.display_input_error("");
                } else {
                    test_stand.awaited_mode = mode;
                }
            } else {
                test_stand.is_awaiting = true;
                test_stand.awaited_mode = mode;
                tui.display_await_mode();
            }
            valid_input = true;
            return;
        }
    }
    tui.display_input_error("Unknown command \"" + tui.input + "\"");
}