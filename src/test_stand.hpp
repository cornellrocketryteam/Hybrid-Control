#ifndef TEST_STAND_HPP_
#define TEST_STAND_HPP_

#include "constants.hpp"
class TestStand {
public:
    TestStand(int handle);

    void sv_on(int num);
    void sv_off(int num);

    void mav_on();
    void mav_off();

    void confirm_mode();

    bool sv_states[5] = {false, false, false, false, false};
    bool mav_state = false;

private:
    void mav_pwm(float dc);
    void sv_pwm(int num);

    void set_sv_states(bool states[]);

    int handle; // TODO: Probably make handle a global variable

    // Pin assignments

    int sv_dio[5] = {SV1_DIO, SV2_DIO, SV3_DIO, SV4_DIO, SV5_DIO};
    int mav_dio = MAV_DIO;
};

#endif