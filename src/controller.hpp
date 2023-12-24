#ifndef CONTROLLER_HPP_
#define CONTROLLER_HPP_

#include "view.hpp"

class Controller {
public:
    Controller(int handle);
    void run();
    void read();

private:
    TestStand test_stand;
    TUI tui;

    void parse_typed_command();
    void parse_mode_command();
};

#endif