#ifndef CONTROLLER_HPP_
#define CONTROLLER_HPP_

#include "view.hpp"

class Controller {
public:
    /**
     * Sets up the controller.
     * @param handle The LabJack handle
     */
    Controller(int handle);

    /**
     * The main control loop. Updates the view and handles commands.
     */
    void run();

    // TODO: Implement
    void read();

private:
    /**
     * The model and view objects.
     */
    TestStand test_stand;
    TUI tui;
    int handle;

    /**
     * Processes a command that is entered through the TUI interface.
     */
    void parse_typed_command();

    /**
     * Processes a command that is entered through the keypad.
     */
    void parse_mode_command();
};

#endif