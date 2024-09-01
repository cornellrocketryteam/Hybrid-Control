#ifndef CONTROLLER_HPP
#define CONTROLLER_HPP

#include "view.hpp"
#include <string>

class Controller {
public:
    /**
     * Sets up the controller.
     * @param handle The LabJack handle
     */
    Controller(int handle);

    /**
     * The main control loop. Updates the view and handles commands.
     * @param running Whether or not the thread should be running
     */
    void run(bool &running);

    /**
     * A separate thread that reads data from certain channels and logs
     * that data to a file.
     * @param running Whether or not the thread should be running
     */
    void read(bool &running);

private:
    /**
     * The model and view objects.
     */
    TestStand test_stand;
    TUI tui;
    int handle;
    double *aData;
    double INIT_SCAN_RATE;
    int SCANS_PER_READ;
    enum { NUM_CHANNELS = 14 };
    double aDataSize;
    bool valid_input;
    std::string input;

    bool data_mark = false;

    std::string filename;

    /**
     * Processes a command that is entered through the TUI interface.
     */
    void parse_typed_command();

    /**
     * Processes a command that is entered through the keypad.
     */
    void parse_mode_command();
};

#endif // CONTROLLER_HPP