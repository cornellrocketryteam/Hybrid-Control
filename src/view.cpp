#include "view.hpp"
#include <iostream>

#define SCREEN_BKGD 1
#define WINDOW_BKGD 2
#define TEXT_COLOR 3
#define WINDOW_SHADOW 4
#define TEXT_ON 5
#define TEXT_OFF 6

TUI::TUI(TestStand *test_stand) {
    this->test_stand = test_stand;
    initscr();
    noecho();
    cbreak();
    curs_set(0);
    start_color();
    // use_default_colors();

    init_pair(SCREEN_BKGD, COLOR_BLACK, COLOR_BLUE);
    init_pair(WINDOW_BKGD, COLOR_WHITE, COLOR_WHITE);
    init_pair(TEXT_COLOR, COLOR_BLACK, COLOR_WHITE);
    init_pair(WINDOW_SHADOW, COLOR_BLACK, COLOR_BLACK);
    init_pair(TEXT_ON, COLOR_GREEN, COLOR_WHITE);
    init_pair(TEXT_OFF, COLOR_RED, COLOR_WHITE);

    bkgd(COLOR_PAIR(SCREEN_BKGD));

    int x_max {getmaxx(stdscr)};
    int y_max {getmaxy(stdscr)};

    valves_shadow = newwin(9, (x_max / 2) - 3, 3, 2);
    wbkgd(valves_shadow, COLOR_PAIR(WINDOW_SHADOW));

    valves_window = newwin(9, (x_max / 2) - 3, 2, 1);
    wbkgd(valves_window, COLOR_PAIR(WINDOW_BKGD));

    sensors_shadow = newwin(9, (x_max / 2) - 3, 18, 2);
    wbkgd(sensors_shadow, COLOR_PAIR(WINDOW_SHADOW));

    sensors_window = newwin(9, (x_max / 2) - 3, 17, 1);
    wbkgd(sensors_window, COLOR_PAIR(WINDOW_BKGD));

    modes_shadow = newwin(10, (x_max / 2) - 2, 3, (x_max / 2) + 2);
    wbkgd(modes_shadow, COLOR_PAIR(WINDOW_SHADOW));

    modes_window = newwin(10, (x_max / 2) - 2, 2, (x_max / 2) + 1);
    wbkgd(modes_window, COLOR_PAIR(WINDOW_BKGD));

    input_window = newwin(5, x_max - 2, y_max - 5, 1);
    wbkgd(input_window, COLOR_PAIR(WINDOW_BKGD));
    keypad(input_window, true);
    nodelay(input_window, true);

    refresh();
}

void TUI::update() {
    werase(valves_window);
    werase(sensors_window);
    werase(modes_window);

        // wclear(input_window);

    wattron(valves_window, COLOR_PAIR(TEXT_COLOR));
    wattron(sensors_window, COLOR_PAIR(TEXT_COLOR));
    wattron(modes_window, COLOR_PAIR(TEXT_COLOR));
    wattron(input_window, COLOR_PAIR(TEXT_COLOR));

    box(valves_window, 0, 0);
    box(sensors_window, 0, 0);
    box(modes_window, 0, 0);
    box(input_window, 0, 0);

    wattron(valves_window, A_BOLD);
    for (int i = 0; i < 5; i++) {
        if (test_stand->sv_states[i]) {
            wattron(valves_window, COLOR_PAIR(TEXT_ON));
            mvwprintw(valves_window, i + 1, 2, "SV %d: %s", i + 1, "ON");
            wattroff(valves_window, COLOR_PAIR(TEXT_ON));
        } else {
            wattron(valves_window, COLOR_PAIR(TEXT_OFF));
            mvwprintw(valves_window, i + 1, 2, "SV %d: %s", i + 1, "OFF");
            wattroff(valves_window, COLOR_PAIR(TEXT_OFF));
        }
    }

    if (test_stand->mav_state) {
        wattron(valves_window, COLOR_PAIR(TEXT_ON));
        mvwprintw(valves_window, 7, 2, "MAV: %s", "ON");
        wattroff(valves_window, COLOR_PAIR(TEXT_ON));
    } else {
        wattron(valves_window, COLOR_PAIR(TEXT_OFF));
        mvwprintw(valves_window, 7, 2, "MAV: %s", "OFF");
        wattroff(valves_window, COLOR_PAIR(TEXT_OFF));
    }

    wattroff(valves_window, A_BOLD);

    if (test_stand->mode == Mode::default_mode) {
        wattron(modes_window, A_BOLD);
        mvwprintw(modes_window, 1, 2, "* Default");
        wattroff(modes_window, A_BOLD);
    } else {
        mvwprintw(modes_window, 1, 4, "Default");
    }
    for (int i = 1; i < 7; i++) {
        if (i == 4) {
            if (supercharged) {
                wattron(modes_window, A_ITALIC);
                mvwprintw(modes_window, i + 2, 4, "Supercharged");
                wattroff(modes_window, A_ITALIC);
            } else {
                mvwprintw(modes_window, i + 2, 4, "Supercharge");
            }
        } else {
            if (test_stand->mode == static_cast<Mode>(i)) {
                wattron(modes_window, A_BOLD);
                mvwprintw(modes_window, i + 2, 2, "* %s", modes[i]);
                wattroff(modes_window, A_BOLD);
            } else {
                mvwprintw(modes_window, i + 2, 4, "%s", modes[i]);
            }
        }
    }

    mvwprintw(sensors_window, 1, 1, "%d", (rand() % 100));
    wattroff(valves_window, COLOR_PAIR(TEXT_COLOR));
    wattroff(sensors_window, COLOR_PAIR(TEXT_COLOR));
    wattroff(modes_window, COLOR_PAIR(TEXT_COLOR));
    wattroff(input_window, COLOR_PAIR(TEXT_COLOR));

    wnoutrefresh(valves_shadow);
    wnoutrefresh(valves_window);

    wnoutrefresh(sensors_shadow);
    wnoutrefresh(sensors_window);

    wnoutrefresh(modes_shadow);
    wnoutrefresh(modes_window);

    wnoutrefresh(input_window);
    doupdate();
    // refresh();
}

bool TUI::get_command() {
    int ch;
    bool is_cmd = false;

    switch (ch = wgetch(input_window)) {
    case KEY_ENTER:
    case 10:
    case 13:
        command_history.insert(command_history.begin(), input);
        keys_up = -1;
        wclear(input_window);
        is_cmd = true;
        break;
    case KEY_BACKSPACE:
    case 127:
    case 8:
        if (input.size() > 0) {
            wclear(input_window);
            input.pop_back();
        }
        break;
    // case 52: // 4
    //     if (input.size() == 0) {
    //         mvwprintw(sensors_window, 5, 5, "52");
    //         wrefresh(sensors_window);

    //         command_history.insert(command_history.begin(), "Default");
    //         keys_up = -1;
    //         wclear(input_window);
    //         is_cmd = true;
    //         input += ch;
    //         break;
    //     }
    //     // fall through
    case KEY_UP:
        if (keys_up < (int)command_history.size() - 1) {
            wclear(input_window);
            keys_up++;
            input = command_history[keys_up];
        }
        break;
    case KEY_DOWN:
        if (keys_up > 0) {
            wclear(input_window);
            keys_up--;
            input = command_history[keys_up];
        } else if (keys_up == 0) {
            wclear(input_window);
            keys_up--;
            input = "";
        }
        break;
    default:
        if (ch != ERR) {
            if (input.size() == 0) {
                if (ch == 52 || ch == 53 || ch == 54 || ch == 465 || ch == 55) {
                    is_cmd = true;
                }
            }
            input += ch;
        }
    }
    wattron(input_window, COLOR_PAIR(TEXT_COLOR));
    mvwprintw(input_window, 1, 1, input.c_str());
    wattroff(input_window, COLOR_PAIR(TEXT_COLOR));

    return is_cmd;
}

void TUI::clear_input() {
    input.clear();
    wclear(input_window);
    wrefresh(input_window);
}