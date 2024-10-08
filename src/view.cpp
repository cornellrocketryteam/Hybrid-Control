#include "view.hpp"
#include "config.hpp"
#include <iostream>

#define SCREEN_BKGD 1
#define WINDOW_BKGD 2
#define TEXT_COLOR 3
#define WINDOW_SHADOW 4
#define TEXT_GREEN 5
#define TEXT_RED 6

TUI::TUI(TestStand *test_stand) {
    this->test_stand = test_stand;
    initscr();
    noecho();
    cbreak();
    curs_set(1);
    start_color();
    // use_default_colors();

    init_pair(SCREEN_BKGD, COLOR_BLACK, COLOR_BLUE);
    init_pair(WINDOW_BKGD, COLOR_WHITE, COLOR_WHITE);
    init_pair(TEXT_COLOR, COLOR_BLACK, COLOR_WHITE);
    init_pair(WINDOW_SHADOW, COLOR_BLACK, COLOR_BLACK);
    init_pair(TEXT_GREEN, COLOR_GREEN, COLOR_WHITE);
    init_pair(TEXT_RED, COLOR_RED, COLOR_WHITE);

    bkgd(COLOR_PAIR(SCREEN_BKGD));

    int x_max {getmaxx(stdscr)};
    int y_max {getmaxy(stdscr)};

    valves_shadow = newwin(10, (x_max / 2) - 4, 3, 3);
    wbkgd(valves_shadow, COLOR_PAIR(WINDOW_SHADOW));

    valves_window = newwin(10, (x_max / 2) - 4, 2, 2);
    wbkgd(valves_window, COLOR_PAIR(WINDOW_BKGD));

    modes_shadow = newwin(10, (x_max / 2) - 4, 3, (x_max / 2) + 2);
    wbkgd(modes_shadow, COLOR_PAIR(WINDOW_SHADOW));

    modes_window = newwin(10, (x_max / 2) - 4, 2, (x_max / 2) + 1);
    wbkgd(modes_window, COLOR_PAIR(WINDOW_BKGD));

    sensors_shadow = newwin(16, x_max - 5, 15, 3);
    wbkgd(sensors_shadow, COLOR_PAIR(WINDOW_SHADOW));

    sensors_window = newwin(16, x_max - 5, 14, 2);
    wbkgd(sensors_window, COLOR_PAIR(WINDOW_BKGD));

    input_window = newwin(2, x_max - 8, y_max - 4, 5);
    wbkgd(input_window, COLOR_PAIR(WINDOW_BKGD));
    keypad(input_window, true);
    nodelay(input_window, true);

    input_container_shadow = newwin(5, x_max - 5, y_max - 5, 3);
    wbkgd(input_container_shadow, COLOR_PAIR(WINDOW_SHADOW));

    input_container_window = newwin(5, x_max - 5, y_max - 6, 2);
    wbkgd(input_container_window, COLOR_PAIR(WINDOW_BKGD));

    wattron(input_container_window, COLOR_PAIR(TEXT_COLOR));
    mvwprintw(input_container_window, 1, 2, "Enter a command below");
    mvwprintw(input_container_window, 3, 2, "> ");

    mvwprintw(input_container_window, 1, x_max - 30, "Data file: data_%d.csv", file_count);
    wattroff(input_container_window, COLOR_PAIR(TEXT_COLOR));

    refresh();
}

void TUI::update(double *data) {
    int x_max {getmaxx(stdscr)};
    werase(valves_window);
    werase(sensors_window);
    werase(modes_window);

    wattron(valves_window, COLOR_PAIR(TEXT_COLOR));
    wattron(sensors_window, COLOR_PAIR(TEXT_COLOR));
    wattron(modes_window, COLOR_PAIR(TEXT_COLOR));
    wattron(input_container_window, COLOR_PAIR(TEXT_COLOR));

    box(valves_window, 0, 0);
    box(sensors_window, 0, 0);
    box(modes_window, 0, 0);
    box(input_container_window, 0, 0);

    // wattron(valves_window, NCURSES_BITS(1U,23));

    wattron(valves_window, A_BOLD);
    mvwprintw(valves_window, 0, (x_max / 4) - 3, " Valves ");
    // wattroff(valves_window, NCURSES_BITS(1U,23));
    for (int i = 0; i < 5; i++) {
        if (test_stand->sv_states[i]) {
            wattron(valves_window, COLOR_PAIR(TEXT_GREEN));
            mvwprintw(valves_window, i + 1, 2, "SV %d: %s", i + 1, "ON");
            wattroff(valves_window, COLOR_PAIR(TEXT_GREEN));
        } else {
            wattron(valves_window, COLOR_PAIR(TEXT_RED));
            mvwprintw(valves_window, i + 1, 2, "SV %d: %s", i + 1, "OFF");
            wattroff(valves_window, COLOR_PAIR(TEXT_RED));
        }
    }

    if (test_stand->mav_state) {
        wattron(valves_window, COLOR_PAIR(TEXT_GREEN));
        mvwprintw(valves_window, 8, 2, "MAV: %s", "ON");
        wattroff(valves_window, COLOR_PAIR(TEXT_GREEN));
    } else {
        wattron(valves_window, COLOR_PAIR(TEXT_RED));
        mvwprintw(valves_window, 8, 2, "MAV: %s", "OFF");
        wattroff(valves_window, COLOR_PAIR(TEXT_RED));
    }

    wattroff(valves_window, A_BOLD);

    wattron(modes_window, A_BOLD);
    mvwprintw(modes_window, 0, (x_max / 4) - 2, " Modes ");
    wattroff(modes_window, A_BOLD);

    if (test_stand->mode == Mode::default_mode) {
        wattron(modes_window, A_BOLD);
        mvwprintw(modes_window, 1, 2, "* Default");
        wattroff(modes_window, A_BOLD);
    } else {
        mvwprintw(modes_window, 1, 4, "Default");
    }
    for (int i = 1; i < 7; i++) {
        if (test_stand->mode == static_cast<Mode>(i)) {
            wattron(modes_window, A_BOLD);
            mvwprintw(modes_window, i + 2, 2, "* %s", modes[i]);
            wattroff(modes_window, A_BOLD);
        } else {
            mvwprintw(modes_window, i + 2, 4, "%s", modes[i]);
        }
    }

    // mvwprintw(sensors_window, 1, 1, "%d", (rand() % 100));
    wattron(sensors_window, A_BOLD);
    mvwprintw(sensors_window, 0, (x_max / 2) - 5, " Sensors ");
    wattroff(sensors_window, A_BOLD);

    // TODO: Finish and clean up - WIP

    wattron(sensors_window, NCURSES_BITS(1U, 23));
    mvwprintw(sensors_window, 1, 2, "Pressure Transducers");
    wattroff(sensors_window, NCURSES_BITS(1U, 23));

    for (int i = 0; i < pt_names.size(); i++) {
        double volt_act = data[i];
        double val = volt_act;

#ifdef USE_LABJACK
        double volt_min = 0;
        double volt_max = 10;
        double val_min = 0;
        double val_max;

        if (i == 0 | i == 5 | i == 6 | i == 7) {
            val_max = 2000;
        } else if (i == 1 | i == 4 | i == 3) {
            val_max = 3000;
        } else if (i == 2) {
            val_max = 1500;
        } else {
            val_max = 0;
        }
        val = test_stand->pt_scale(volt_act, volt_min, volt_max, val_min, val_max);
#endif
        mvwprintw(sensors_window, i + 3, 2, "%s   %f PSI", pt_names[i].c_str(), val);
    }

    wattron(sensors_window, NCURSES_BITS(1U, 23));
    mvwprintw(sensors_window, 1, 70, "Thermocouples");
    wattroff(sensors_window, NCURSES_BITS(1U, 23));

    for (int i = 0; i < tc_names.size(); i++) {
        double volt_act = data[pt_names.size() + i];
        double val = volt_act;
#ifdef USE_LABJACK
        val = test_stand->tc_scale(volt_act);
#endif

        mvwprintw(sensors_window, i + 3, 70, "%s   %f F", tc_names[i].c_str(), val);
    }

    wattron(sensors_window, NCURSES_BITS(1U, 23));
    mvwprintw(sensors_window, 7, 70, "Load Cells");
    wattroff(sensors_window, NCURSES_BITS(1U, 23));

    for (int i = 0; i < lc_names.size(); i++) {
        double volt_act = data[pt_names.size() + tc_names.size() + fm_names.size() + i];
        double val = volt_act;
#ifdef USE_LABJACK
        double m, b;
        if (i == 0) {
            m = 31.27993035;
            b = -0.2654580671;
        } else if (i == 1) {
            m = 60.25906654;
            b = -0.02513497142;
        } else {
            m = 0;
            b = 0;
        }
        val = test_stand->lc_scale(volt_act, m, b);
#endif
        mvwprintw(sensors_window, i + 9, 70, "%s   %f lbf", lc_names[i].c_str(), val);
    }

    wattron(sensors_window, NCURSES_BITS(1U, 23));
    mvwprintw(sensors_window, 12, 2, "Flowmeters");
    wattroff(sensors_window, NCURSES_BITS(1U, 23));

    for (int i = 0; i < fm_names.size(); i++) {
        mvwprintw(sensors_window, i + 14, 2, "%s   %f GPM", fm_names[i].c_str(), data[pt_names.size() + tc_names.size() + i]);
    }

    mvwprintw(input_container_window, 3, 2, "> ");
    mvwprintw(input_container_window, 1, x_max - 30, "Data file: data_%d.csv", file_count);
    wattroff(valves_window, COLOR_PAIR(TEXT_COLOR));
    wattroff(sensors_window, COLOR_PAIR(TEXT_COLOR));
    wattroff(modes_window, COLOR_PAIR(TEXT_COLOR));
    wattroff(input_container_window, COLOR_PAIR(TEXT_COLOR));

    wnoutrefresh(valves_shadow);
    wnoutrefresh(valves_window);

    wnoutrefresh(sensors_shadow);
    wnoutrefresh(sensors_window);

    wnoutrefresh(modes_shadow);
    wnoutrefresh(modes_window);

    wnoutrefresh(input_container_shadow);
    wnoutrefresh(input_container_window);
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
                for (int ascii : mode_ascii_mappings) {
                    if (ch == ascii) {
                        is_cmd = true;
                        break;
                    }
                }
                for (int ascii : valve_ascii_mappings) {
                    if (ch == ascii) {
                        is_cmd = true;
                        break;
                    }
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

void TUI::display_message(std::string msg, bool error) {
    werase(input_container_window);

    if (error) {
        wattron(input_container_window, COLOR_PAIR(TEXT_RED));
    } else {
        wattron(input_container_window, COLOR_PAIR(TEXT_COLOR));
    }

    mvwprintw(input_container_window, 1, 2, msg.c_str());

    if (error) {
        wattroff(input_container_window, COLOR_PAIR(TEXT_RED));
    } else {
        wattroff(input_container_window, COLOR_PAIR(TEXT_COLOR));
    }

    wrefresh(input_container_window);
}

void TUI::display_await_mode() {
    werase(input_container_window);
    wattron(input_container_window, COLOR_PAIR(TEXT_COLOR));
    mvwprintw(input_container_window, 1, 2, "Confirm");
    wattron(input_container_window, A_BOLD);
    mvwprintw(input_container_window, 1, 10, "%s", modes[static_cast<int>(test_stand->awaited_mode)]);
    wattroff(input_container_window, COLOR_PAIR(TEXT_COLOR) | A_BOLD);
    wrefresh(input_container_window);
}

void TUI::display_await_valve() {
    werase(input_container_window);
    wattron(input_container_window, COLOR_PAIR(TEXT_COLOR));
    mvwprintw(input_container_window, 1, 2, "Confirm");
    wattron(input_container_window, A_BOLD);
    mvwprintw(input_container_window, 1, 10, "%s", valves[test_stand->awaited_valve]);
    wattroff(input_container_window, COLOR_PAIR(TEXT_COLOR) | A_BOLD);
    wrefresh(input_container_window);
}

void TUI::clear_input() {
    input.clear();
    wclear(input_window);
    wrefresh(input_window);
}