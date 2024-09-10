#ifndef VIEW_HPP
#define VIEW_HPP

#include <curses.h>
#include <string>
#include <vector>

#include "test_stand.hpp"

class TUI {
public:
    /**
     * Initializes and sets up the view.
     * @param test_stand The model to pull data from
     */
    TUI(TestStand *test_stand);

    /**
     * Queries the current state of the model and updates the view.
     */
    void update(double *data);

    /**
     * Parses a keystroke and updates the input window.
     * @return True if this is a command the controller must process, false otherwise
     */
    bool get_command();

    /**
     * Clears the internal input buffer and updates the input window view.
     */
    void clear_input();

    /**
     * Displays a message atop the input window.
     * @param msg The message to display
     * @param error Whether or not to display this message in red text
     */
    void display_message(std::string msg, bool error = false);

    /**
     * Displays the mode awaiting confirmation atop the input window.
     */
    void display_await_mode();

    /**
     * Displays the valve awaiting confirmation atop the input window.
     */
    void display_await_valve();

    /**
     * The input buffer that is updated with every keystroke.
     */
    std::string input;

    // TODO: Temporary fix, this is not elegant
    int file_count;

private:
    /**
     * The model to pull data from.
     */
    TestStand *test_stand;

    /**
     * Curses-specific variables
     */
    WINDOW *valves_window;
    WINDOW *sensors_window;

    WINDOW *modes_window;
    WINDOW *input_window;
    WINDOW *input_container_window;

    WINDOW *valves_shadow;
    WINDOW *sensors_shadow;
    WINDOW *modes_shadow;
    WINDOW *input_container_shadow;

    /**
     * Command history storage.
     */
    std::vector<std::string> command_history;

    /**
     * Tracks the current index of the command history, if applicable.
     *
     * Will never be greater than the command history length
     * Will be -1 if not currently scrolling through command history
     */
    int keys_up = -1;

    // TODO: Probably move mode names to get directly from config
    char const *modes[7] = {"Default", "Prefire purge tanks", "Prefire purge engine", "Fill", "Close vent", "Fire", "Postfire purge engine"};

    char const *valves[6] = {"SV 1", "SV 2", "SV 3", "SV 4", "SV 5", "MAV"};
};

#endif // VIEW_HPP