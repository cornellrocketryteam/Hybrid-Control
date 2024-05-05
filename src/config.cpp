#include "config.hpp"

// TODO: Check compatability with non-macOS computers
int mode_ascii_mappings[7] = {52, 53, 54, 43, 55, 56, 57};

int valve_ascii_mappings[6] = {48, 49, 50, 51, 46, 45};

std::vector<std::string> pt_names = {
    "PT 1: Purge Downstream:      ",
    "PT 2: Engine Chamber:        ",
    "PT 3: N2O Tank:              ",
    "PT 4: Purge Tank:            ",
    "PT 5: Supercharge Tank:      ",
    "PT 6: Run Tank:              ",
    "PT 7: Injector Manifold:     ",
    "PT 8: Supercharge Downstream:"};

std::vector<std::string> tc_names = {
    "TC 1: Run Tank: ",
    "TC 2: Engine:   ",
    "TC 3: MAV Inlet:",
};

std::vector<std::string> lc_names = {
    "LC 1: Thrust:     ",
    "LC 2: Tank Weight:",
};

std::vector<std::string> fm_names = {
    "FM 1:",
};