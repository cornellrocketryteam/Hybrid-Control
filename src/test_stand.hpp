#ifndef TEST_STAND_HPP_
#define TEST_STAND_HPP_

class TestStand {
public:
    TestStand();

    void sv_on(int num);
    void sv_off(int num);

    void mav_on();
    void mav_off();

    void confirm_mode();

    bool sv_states[5] = {false, false, false, false, false};
    bool mav_state = false;

private:
    void mav_actuate(float dc);
    void sv_pwm(int num);

    void set_sv_states(bool states[]);

    // Pin assignments

    int sv_dio[5] = {1, 0, 2, 3, 4};
    int mav_dio = 5;
};

#endif