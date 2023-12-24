#ifndef VIEW_HPP_
#define VIEW_HPP_

#include <curses.h>
#include <string>

#include "test_stand.hpp"

class TUI {
public:
    TUI(TestStand *test_stand);
    void update();
    // int get_input();
    void await_mode();
    void end_await();
    void to_mode();
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

    // Test stand-specific variables
    int mode = 0;
    char const *modes[7] = {"Default", "Prefire purge tanks", "Prefire purge engines", "Fill", "Supercharge", "Postfire purge engine", "Fire"};
    bool supercharged = false;
};

#endif