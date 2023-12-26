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
    void await_mode();
    void end_await();
    void clear_input();

    bool get_command();

    std::string input;

private:
    void convert_data();

    TestStand *test_stand;

    // Curses-specific variables
    WINDOW *valves_window;
    WINDOW *sensors_window;

    WINDOW *modes_window;
    WINDOW *input_window;

    WINDOW *valves_shadow;
    WINDOW *sensors_shadow;
    WINDOW *modes_shadow;

    std::vector<std::string> command_history;
    int keys_up = -1;

    // Test stand-specific variables: Probably move modes to get directly from config
    char const *modes[7] = {"Default", "Prefire purge tanks", "Prefire purge engines", "Fill", "Supercharge", "Postfire purge engine", "Fire"};
    bool supercharged = false;
};

#endif