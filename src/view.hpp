#ifndef VIEW_HPP_
#define VIEW_HPP_

#include <curses.h>
#include <string>
#include <vector>

#include "test_stand.hpp"

class TUI {
public:
    TUI(TestStand *test_stand);

    void update();
    bool get_command();
    void clear_input();

    void display_input_error(std::string error);
    void display_await_mode();

    std::string input;

private:
    void convert_data();

    TestStand *test_stand;

    // Curses-specific variables
    WINDOW *valves_window;
    WINDOW *sensors_window;

    WINDOW *modes_window;
    WINDOW *input_window;
    WINDOW *input_container_window;

    WINDOW *valves_shadow;
    WINDOW *sensors_shadow;
    WINDOW *modes_shadow;
    WINDOW *input_container_shadow;

    std::vector<std::string> command_history;
    int keys_up = -1;

    // Probably move mode names to get directly from config
    char const *modes[7] = {"Default", "Prefire purge tanks", "Prefire purge engine", "Fill", "Supercharge", "Postfire purge engine", "Fire"};
};

#endif