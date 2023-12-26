#include "test_stand.hpp"
#include "config.hpp"
#include <LabJackM.h>
// #include <LJM_Utilities.h>
#include <cstdio>

TestStand::TestStand(int handle) : handle(handle) {
}

void TestStand::sv_on(int num) {
    sv_states[num - 1] = true;

#ifdef USE_LABJACK
    char fio_name[4];
    snprintf(fio_name, 4, "FIO%d", num - 1);

    (void)LJM_eWriteName(handle, fio_name, 1);
    // TODO: PWM on timer
#endif
}

void TestStand::sv_off(int num) {
    sv_states[num - 1] = false;

#ifdef USE_LABJACK
    char fio_name[4];
    snprintf(fio_name, 4, "FIO%d", num - 1);

    char dio_ef_enable[14];
    snprintf(dio_ef_enable, 14, "DIO%d_EF_ENABLE", num - 1);

    (void)LJM_eWriteName(handle, fio_name, 0);
    (void)LJM_eWriteName(handle, dio_ef_enable, 0);
#endif
}

void TestStand::sv_pwm(int num) {
}

void TestStand::mav_on() {
    mav_state = true;

#ifdef USE_LABJACK
    mav_pwm(25.0);
#endif
}

void TestStand::mav_off() {
    mav_state = false;

#ifdef USE_LABJACK
    mav_pwm(60.0);
#endif
}

void TestStand::mav_pwm(float dc) {
    float config_a = dc * MAV_ROLL_VALUE / 100;

    char dio_ef_enable[14];
    snprintf(dio_ef_enable, 14, "DIO%d_EF_ENABLE", MAV_DIO);

    char dio_ef_config_a[15];
    snprintf(dio_ef_config_a, 15, "DIO%d_EF_CONFIG_A", MAV_DIO);

    const int NUM_FRAMES = 5;
    const char *names[NUM_FRAMES] = {"DIO_EF_CLOCK0_ROLL_VALUE", "DIO_EF_CLOCK0_ENABLE", dio_ef_enable, dio_ef_config_a, dio_ef_enable};

    double values[NUM_FRAMES] = {MAV_ROLL_VALUE, 1, 0, config_a, 1};

    // int errorAddress = INITIAL_ERR_ADDRESS;
    int errorAddress;

    (void)LJM_eWriteNames(handle, NUM_FRAMES, names, values, &errorAddress);
    // ErrorCheckWithAddress(err, errorAddress, "LJM_eWriteNames"); TODO: Talk to LabJack people about error in util header file
}

void TestStand::set_sv_states(std::string mask) {
    for (int i = 0; i < mask.size(); i++) {
        if (mask[i] - '0') {
            sv_on(i + 1);
        } else {
            sv_off(i + 1);
        }
    }
}

void TestStand::to_mode(Mode mode) {
    switch (mode) {
    case Mode::prefire_purge_tanks:
        if (!tanks_purging) {
            set_sv_states("01001");
        } else {
            set_sv_states("00000");
        }
        break;
    case Mode::prefire_purge_engine:
        if (!engine_purging) {
            set_sv_states("10000");
        } else {
            set_sv_states("00000");
        }
        break;
    case Mode::fill:
        if (!filling) {
            set_sv_states("00100");
        } else {
            set_sv_states("00000");
        }
        break;
    case Mode::supercharge:
        set_sv_states("00010");
        break;
    case Mode::postfire_purge_engine:
        set_sv_states("01010");
        break;
    case Mode::fire:
        set_sv_states("00010");
        mav_on();
        break;
    default:
        set_sv_states("00000");
        mav_off();
    }

    this->mode = mode;
}