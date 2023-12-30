#include "controller.hpp"
#include "config.hpp"
#include "test_stand.hpp"
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

Controller::Controller(int handle) : test_stand(TestStand(handle)), tui(TUI(&test_stand)) {
}

// Instruct the view to update and process any input commands
void Controller::run() {
    while (true) {
        tui.update();

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
        } else if (tokens[2] == "off") {
            test_stand.sv_off(sv);
        } else {
            tui.display_input_error("Unknown SV operation \"" + tokens[2] + "\"");
        }
    } else if (tui.input == "mav on") {
        test_stand.mav_on();
    } else if (tui.input == "mav off") {
        test_stand.mav_off();
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
            return;
        }
    }
    tui.display_input_error("Unknown command \"" + tui.input + "\"");
}