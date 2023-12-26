#ifndef CONFIG_HPP_
#define CONFIG_HPP_

#define SV1_DIO 1
#define SV2_DIO 0
#define SV3_DIO 2
#define SV4_DIO 3
#define SV5_DIO 4

#define MAV_DIO 5

#define MAV_ROLL_VALUE 240240.24024

enum class Mode : int {
    default_mode = 0,
    prefire_purge_tanks,
    prefire_purge_engine,
    fill,
    supercharge,
    postfire_purge_engine,
    fire
};

// TODO: Add some kind of mapping between Mode and ASCII character, maybe just modify the existing enum class's ints

#endif // CONFIG_HPP_