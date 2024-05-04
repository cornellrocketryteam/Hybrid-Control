#include "test_stand.hpp"
#include <chrono>
#include <cstdio>
#include <thread>

TestStand::TestStand(int handle) : handle(handle) {
}

void TestStand::sv_toggle(int num) {
    if (sv_states[num - 1]) {
        sv_off(num);
    } else {
        sv_on(num);
    }
}

void TestStand::sv_on(int num) {
    if (num == 4) { // NOTE: SV 4 is never being actuated
        return;
    }
    sv_states[num - 1] = true;

#ifdef USE_LABJACK
    char fio_name[5];
    snprintf(fio_name, 5, "FIO%d", sv_dio[num - 1]);

    err = LJM_eWriteName(handle, fio_name, 1);
    ErrorCheckWithAddress(err, error_address, "LJM_eWriteNames");

    std::thread timer_thread([this, num]() {
        this->sv_pwm(num);
    });
    timer_thread.detach();
#endif
}

void TestStand::sv_off(int num) {
    sv_states[num - 1] = false;

#ifdef USE_LABJACK
    char fio_name[5];
    snprintf(fio_name, 5, "FIO%d", sv_dio[num - 1]);

    char dio_ef_enable[16];
    snprintf(dio_ef_enable, 16, "DIO%d_EF_ENABLE", sv_dio[num - 1]);

    err = LJM_eWriteName(handle, dio_ef_enable, 0);
    ErrorCheckWithAddress(err, error_address, "LJM_eWriteName");

    err = LJM_eWriteName(handle, fio_name, 0);
    ErrorCheckWithAddress(err, error_address, "LJM_eWriteName");
#endif
}

void TestStand::mav_toggle() {
    if (mav_state) {
        mav_off();
    } else {
        mav_on();
    }
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

    char dio_ef_enable[15];
    snprintf(dio_ef_enable, 15, "DIO%d_EF_ENABLE", MAV_DIO);

    char dio_ef_config_a[17];
    snprintf(dio_ef_config_a, 17, "DIO%d_EF_CONFIG_A", MAV_DIO);

    const int NUM_FRAMES = 5;
    const char *names[NUM_FRAMES] = {"DIO_EF_CLOCK0_ROLL_VALUE", "DIO_EF_CLOCK0_ENABLE", dio_ef_enable, dio_ef_config_a, dio_ef_enable};
    double values[NUM_FRAMES] = {MAV_ROLL_VALUE, 1, 0, config_a, 1};

    err = WriteNames(handle, NUM_FRAMES, names, values, &error_address);
    ErrorCheckWithAddress(err, error_address, "LJM_eWriteNames");
}

void TestStand::sv_pwm(int num) {
    std::this_thread::sleep_for(std::chrono::milliseconds(150));

    int pwm_dio = sv_dio[num - 1];
    float config_a = SV_DC * SV_ROLL_VALUE / 100;

    char dio_ef_enable[15];
    snprintf(dio_ef_enable, 15, "DIO%d_EF_ENABLE", pwm_dio);

    char dio_ef_config_a[17];
    snprintf(dio_ef_config_a, 17, "DIO%d_EF_CONFIG_A", pwm_dio);

    const int NUM_FRAMES = 5;
    const char *names[NUM_FRAMES] = {"DIO_EF_CLOCK0_ROLL_VALUE", "DIO_EF_CLOCK0_ENABLE", dio_ef_enable, dio_ef_config_a, dio_ef_enable};
    double values[NUM_FRAMES] = {SV_ROLL_VALUE, 1, 0, config_a, 1};

    err = WriteNames(handle, NUM_FRAMES, names, values, &error_address);
    ErrorCheckWithAddress(err, error_address, "LJM_eWriteNames");
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
        supercharged = true;
        set_sv_states("00010");
        break;
    case Mode::postfire_purge_engine:
        set_sv_states("10000");
        break;
    case Mode::fire:
        set_sv_states("00000");
        mav_on();
        break;
    default:
        set_sv_states("00000");
        mav_off();
    }

    this->mode = mode;
}