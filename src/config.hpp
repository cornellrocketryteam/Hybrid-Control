#ifndef CONFIG_HPP_
#define CONFIG_HPP_

#include <string>
#include <vector>

/**
 * Pin assignments.
 */
#define SV1_DIO 1
#define SV2_DIO 0
#define SV3_DIO 2
#define SV4_DIO 3
#define SV5_DIO 4

#define MAV_DIO 5

#define MAV_ROLL_VALUE 240240.24024

/**
 * Defines each mode
 */
enum class Mode : int {
    default_mode = 0,
    prefire_purge_tanks,
    prefire_purge_engine,
    fill,
    supercharge,
    postfire_purge_engine,
    fire
};

/**
 * The ASCII key mappings for each mode.
 */
extern int ascii_mappings[7];

/**
 * Descriptive names for each sensor to display on the TUI.
 */
extern std::vector<std::string> pt_names;
extern std::vector<std::string> tc_names;
extern std::vector<std::string> lc_names;
extern std::vector<std::string> fm_names;

#endif // CONFIG_HPP_