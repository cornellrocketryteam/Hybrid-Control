#include "controller.hpp"
#include "test_stand.hpp"
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

Controller::Controller() : test_stand(TestStand()), tui(TUI(&test_stand)) {
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
            return;
        }

        if (tokens[2] == "on") {
            test_stand.sv_states[sv - 1] = true;
        } else if (tokens[2] == "off") {
            test_stand.sv_states[sv - 1] = false;
        }
    }
    if (tui.input == "mav on") {
        test_stand.mav_state = true;
    }
    if (tui.input == "mav off") {
        test_stand.mav_state = false;
    }
}

void Controller::parse_mode_command() {
}